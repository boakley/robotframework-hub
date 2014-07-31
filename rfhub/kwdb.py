"""keywordtable - an SQLite database of keywords

Keywords can be loaded from resource files, test suite files,
and libdoc-formatted xml, or from python libraries. These
are referred to as "collections".

"""

import sqlite3
import os
from robot.libdocpkg import LibraryDocumentation
import robot.libraries
import logging
import json
import re
import sys

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

"""
Note: It seems to be possible for watchdog to fire an event
when a file is modified, but before the file is _finished_
being modified (ie: you get the event when some other program
writes the first byte, rather than waiting until the other
program closes the file)

For that reason, we might want to mark a collection as
"dirty", and only reload after some period of time has
elapsed? I haven't yet experienced this problem, but
I haven't done extensive testing.
"""

class WatchdogHandler(PatternMatchingEventHandler):
    patterns = ["*.robot", "*.txt", "*.py"]
    def __init__(self, kwdb, path):
        PatternMatchingEventHandler.__init__(self)
        self.kwdb = kwdb
        self.path = path

    def on_created(self, event):
        # monitor=False because we're already monitoring
        # ancestor of the file that was created. Duh.
        self.kwdb.add(event.src_path, monitor=False)

    def on_deleted(self, event):
        # FIXME: need to implement this
        pass

    def on_modified(self, event):
        self.kwdb.on_change(event.src_path, event.event_type)

class KeywordTable(object):
    """A SQLite database of keywords"""

    def __init__(self, dbfile=":memory:"):
        self.db = sqlite3.connect(dbfile, check_same_thread=False)
        self.log = logging.getLogger(__name__)
        self._create_db()
#        self.log.warning("I'm warnin' ya!")

        # set up watchdog observer to monitor changes to
        # keyword files (or more correctly, to directories
        # of keyword files)
        self.observer = Observer()
        self.observer.start()

    def add(self, name, monitor=True):
        """Add a folder, library (.py) or resource file (.robot, .txt) to the database
        """

        if os.path.isdir(name):
            if (not os.path.basename(name).startswith(".")):
                self.add_folder(name)

        elif os.path.isfile(name):
            if ((self._looks_like_resource_file(name)) or
                (self._looks_like_libdoc_file(name)) or
                (self._looks_like_library_file(name))):
                self.add_file(name)
        else:
            # let's hope it's a library name!
            self.add_library(name)

    def on_change(self, path, event_type):
        """Respond to changes in the file system

        This method will be given the path to a file that
        has changed on disk. We need to reload the keywords
        from that file
        """
        # I can do all this work in a sql statement, but
        # for debugging it's easier to do it in stages.
        sql = """SELECT collection_id
                 FROM collection_table
                 WHERE path == ?
        """
        cursor = self._execute(sql, (path,))
        results = cursor.fetchall()
        # there should always be exactly one result, but
        # there's no harm in using a loop to process the
        # single result
        for result in results:
            collection_id = result[0]
            # remove all keywords in this collection
            sql = """DELETE from keyword_table
                     WHERE collection_id == ?
            """
            cursor = self._execute(sql, (collection_id,))
            self._load_keywords(collection_id, path=path)

    def _load_keywords(self, collection_id, path=None, libdoc=None):
        """Load a collection of keywords

           One of path or libdoc needs to be passed in...
        """
        if libdoc is None and path is None:
            raise(Exception("You must provide either a path or libdoc argument"))

        if libdoc is None:
            libdoc = LibraryDocumentation(path)

        if len(libdoc.keywords) > 0:
            for keyword in libdoc.keywords:
                self._add_keyword(collection_id, keyword.name, keyword.doc, keyword.args)

    def add_file(self, path):
        """Add a resource file or library file to the database"""
        libdoc = LibraryDocumentation(path)
        if len(libdoc.keywords) > 0:
            collection_id = self.add_collection(path, libdoc.name, libdoc.type,
                                                libdoc.doc, libdoc.version,
                                                libdoc.scope, libdoc.named_args,
                                                libdoc.doc_format)
            self._load_keywords(collection_id, libdoc=libdoc)

    def add_library(self, name):
        """Add a library to the database

        This method is for adding a library by name (eg: "BuiltIn")
        rather than by a file.
        """
        libdoc = LibraryDocumentation(name)
        if len(libdoc.keywords) > 0:
            # FIXME: figure out the path to the library file
            collection_id = self.add_collection(None, libdoc.name, libdoc.type,
                                                libdoc.doc, libdoc.version,
                                                libdoc.scope, libdoc.named_args,
                                                libdoc.doc_format)
            self._load_keywords(collection_id, libdoc=libdoc)

    def add_folder(self, dirname, watch=True):
        """Recursively add all files in a folder to the database

        By "all files" I mean, "all files that are resource files
        or library files". It will silently ignore files that don't
        look like they belong in the database. Pity the fool who
        uses non-standard suffixes.

        N.B. folders with names that begin with '." will be skipped
        """
        for filename in os.listdir(dirname):
            path = os.path.join(dirname, filename)
            (basename, ext) = os.path.splitext(filename.lower())

            try:
                if (os.path.isdir(path)):
                    if (not basename.startswith(".")):
                        if os.access(path, os.R_OK):
                            self.add_folder(path, watch=False)
                else:
                    if (ext in (".xml", ".robot", ".txt", ".py")):
                        if os.access(path, os.R_OK):
                            self.add(path)
            except Exception, e:
                # I really need to get the logging situation figured out.
                print "bummer:", str(e)

        # FIXME:
        # instead of passing a flag around, I should just keep track
        # of which folders we're watching, and don't add wathers for
        # any subfolders. That will work better in the case where
        # the user accidentally starts up the hub giving the same
        # folder, or a folder and it's children, on the command line...
        if watch:
            # add watcher on normalized path
            dirname = os.path.abspath(dirname)
            event_handler = WatchdogHandler(self, dirname)
            self.observer.schedule(event_handler, dirname, recursive=True)

    def add_collection(self, path, c_name, c_type, c_doc, c_version="unknown",
                       c_scope="", c_namedargs="yes", c_doc_format="ROBOT"):
        """Insert data into the collection table"""
        if path is not None:
            # We want to store the normalized form of the path in the
            # database
            path = os.path.abspath(path)

        cursor = self.db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO collection_table
                (name, type, version, scope, namedargs, path, doc, doc_format)
            VALUES
                (?,?,?,?,?,?,?,?)
        """, (c_name, c_type, c_version, c_scope, c_namedargs, path, c_doc, c_doc_format))
        collection_id = cursor.lastrowid
        return collection_id

    def add_installed_libraries(self, extra_libs = ["Selenium2Library",
                                                    "SudsLibrary",
                                                    "RequestsLibrary"]):
        """Add any installed libraries that we can find

        We do this by looking in the `libraries` folder where
        robot is installed. If you have libraries installed
        in a non-standard place, this won't pick them up.
        """

        libdir = os.path.dirname(robot.libraries.__file__)
        loaded = []
        for filename in os.listdir(libdir):
            if filename.endswith(".py") or filename.endswith(".pyc"):
                libname, ext = os.path.splitext(filename)
                if (libname.lower() not in loaded and
                    not self._should_ignore(libname)):

                    try:
                        self.add(libname)
                        loaded.append(libname.lower())
                    except Exception, e:
                        # need a better way to log this...
                        self.log.debug("unable to add library: " + str(e))

        # I hate how I implemented this, but I don't think there's
        # any way to find out which installed python packages are
        # robot libraries.
        for library in extra_libs:
            if (library.lower() not in loaded and
                not self._should_ignore(library)):
                try:
                    self.add(library)
                    loaded.append(library.lower())
                except Exception, e:
                    self.log.debug("unable to add external library %s: %s" % \
                                   (library, str(e)))

    def get_collection(self, name):
        """Get a specific collection"""
        sql = """SELECT collection.name, collection.path,
                        collection.doc,
                        collection.version, collection.scope,
                        collection.namedargs,
                        collection.doc_format
                 FROM collection_table as collection
                 WHERE name like ?
        """
        cursor = self._execute(sql, (name,))
        # need to do more than return just the name; should
        # return version, path (?), list of keywords (?)
        sql_result = cursor.fetchone()
        return {
            "name": sql_result[0],
            "path": sql_result[1],
            "doc":  sql_result[2],
            "version": sql_result[3],
            "scope":   sql_result[4],
            "namedargs": sql_result[5],
            "doc_format": sql_result[6]
        }
        return sql_result

    def get_collections(self, pattern="*", libtype="*"):
        """Returns a list of collection name/summary tuples"""

        sql = """SELECT collection.name, collection.doc,
                        collection.type, collection.path
                 FROM collection_table as collection
                 WHERE name like ?
                 AND type like ?
                 ORDER BY collection.name
              """

        cursor = self._execute(sql, (self._glob_to_sql(pattern),
                                     self._glob_to_sql(libtype)))
        sql_result = cursor.fetchall()

        return [{"name": result[0],
                 "synopsis": result[1].split("\n")[0],
                 "type": result[2],
                 "path": result[3]
             } for result in sql_result]

    def get_keyword_data(self, collection_name):
        sql = """SELECT keyword.name, keyword.args, keyword.doc
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND collection.name like ?
                 ORDER BY keyword.name
              """
        cursor = self._execute(sql, (collection_name,))
        return cursor.fetchall()

    def get_keyword(self, library, name):
        """Get a specific keyword from a library"""
        sql = """SELECT keyword.name, keyword.args, keyword.doc, collection.name
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND collection.name like ?
                 AND keyword.name like ?
              """
        cursor = self._execute(sql, (library,name))
        # We're going to assume no library has duplicate keywords
        # While that in theory _could_ happen, it never _should_,
        # and you get what you deserve if it does.
        row = cursor.fetchone()
        if row is not None:
            return {"name": row[0],
                    "args": json.loads(row[1]),
                    "doc": row[2],
                    "library": row[3] # should this be a URL to the library? Probably
            }
        return {}

    def get_keyword_hierarchy(self, pattern="*"):
        """Returns all keywords that match a glob-style pattern

        The result is a list of dictionaries, sorted by collection
        name.

        The pattern matching is insensitive to case. The function
        returns a list of (library_name, keyword_name,
        keyword_synopsis tuples) sorted by keyword name

        """

        sql = """SELECT collection.name, keyword.name, keyword.doc
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND keyword.name like ?
                 ORDER by collection.name, keyword.name
             """
        cursor = self._execute(sql, (self._glob_to_sql(pattern),))
        libraries = []
        current_library = None
        for row in cursor.fetchall():
            (c_name, k_name, k_doc) = row
            if c_name != current_library:
                current_library = c_name
                libraries.append({"name": c_name, "keywords": []})
            libraries[-1]["keywords"].append({"name": k_name, "doc": k_doc})
        return libraries

    def search(self, pattern="*"):
        """Perform a pattern-based search on keyword names and documentation

        The pattern matching is insensitive to case. The function
        returns a list of (library_name, keyword_name,
        keyword_synopsis tuples) sorted by keyword name

        """
        sql = """SELECT collection.name, keyword.name, keyword.doc
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND (keyword.name like ? OR keyword.doc like ?)
                 ORDER by collection.name, keyword.name
             """
        pattern = self._glob_to_sql(pattern)
        cursor = self._execute(sql, (pattern,pattern))
        result = [(row[0], row[1], row[2].strip().split("\n")[0])
                  for row in cursor.fetchall()]
        return list(set(result))

    def get_keywords(self, pattern="*"):
        """Returns all keywords that match a glob-style pattern

        The pattern matching is insensitive to case. The function
        returns a list of (library_name, keyword_name,
        keyword_synopsis tuples) sorted by keyword name

        """

        sql = """SELECT collection.name,
                        keyword.name, keyword.doc, keyword.args
                 FROM collection_table as collection
                 JOIN keyword_table as keyword
                 WHERE collection.collection_id == keyword.collection_id
                 AND keyword.name like ?
                 ORDER by collection.name, keyword.name
             """
        pattern = self._glob_to_sql(pattern)
        cursor = self._execute(sql, (pattern,))
        result = [(row[0], row[1], row[2], row[3])
                  for row in cursor.fetchall()]
        return list(set(result))

    def reset(self):
        """Remove all data from the database, but leave the tables intact"""
        self._execute("DELETE FROM collection_table")
        self._execute("DELETE FROM keyword_table")

    def _looks_like_library_file(self, name):
        return name.endswith(".py")

    def _looks_like_libdoc_file(self, name):
        """Return true if an xml file looks like a libdoc file"""
        # inefficient since we end up reading the file twice,
        # but it's fast enough for our purposes, and prevents
        # us from doing a full parse of files that are obviously
        # not libdoc files
        if name.lower().endswith(".xml"):
            with open(name, "r") as f:
                # read the first few lines; if we don't see
                # what looks like libdoc data, return false
                data = f.read(200)
                index = data.lower().find("<keywordspec ")
                if index > 0:
                    return True
        return False

    def _looks_like_resource_file(self, name):
        """Return true if the file has a keyword table but not a testcase table"""
        # inefficient since we end up reading the file twice,
        # but it's fast enough for our purposes, and prevents
        # us from doing a full parse of files that are obviously
        # not robot files

        found_keyword_table = False
        if (name.lower().endswith(".robot") or
            name.lower().endswith(".txt")) :

            with open(name, "r") as f:
                data = f.read()
                for match in re.finditer(r'^\*+\s*(Test Cases?|(?:User )?Keywords?)',
                                         data, re.MULTILINE|re.IGNORECASE):
                    if (re.match(r'Test Cases?', match.group(1), re.IGNORECASE)):
                        # if there's a test case table, it's not a keyword file
                        return False

                    if (not found_keyword_table and
                        re.match(r'(User )?Keywords?', match.group(1), re.IGNORECASE)):
                        found_keyword_table = True
        return found_keyword_table

    def _should_ignore(self, name):
        """Return True if a given library name should be ignored

        This is necessary because not all files we find in the library
        folder are libraries. I wish there was a public robot API
        for "give me a list of installed libraries"...
        """
        _name = name.lower()
        return (_name.startswith("deprecated") or
                _name.startswith("_") or
                _name in ("remote", "reserved",
                          "dialogs_py", "dialogs_ipy", "dialogs_jy"))

    def _execute(self, *args):
        """Execute an SQL query

        This exists because I think it's tedious to get a cursor and
        then use a cursor.
        """
        cursor = self.db.cursor()
        cursor.execute(*args)
        return cursor

    def _add_keyword(self, collection_id, name, doc, args):
        """Insert data into the keyword table

        'args' should be a list, but since we can't store a list in an
        sqlite database we'll make it json we can can convert it back
        to a list later.
        """
        argstring = json.dumps(args)
        self.db.execute("""
            INSERT OR REPLACE INTO keyword_table
                (collection_id, name, doc, args)
            VALUES
                (?,?,?,?)
        """, (collection_id, name, doc, argstring))

    def _create_db(self):

        if not self._table_exists("collection_table"):
            self.db.execute("""
                CREATE TABLE collection_table
                (collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE UNIQUE,
                 type          COLLATE NOCASE,
                 version       TEXT,
                 scope         TEXT,
                 namedargs     TEXT,
                 path          TEXT,
                 doc           TEXT,
                 doc_format    TEXT)
            """)
            self.db.execute("""
                CREATE INDEX collection_index
                ON collection_table (name)
            """)

        if not self._table_exists("keyword_table"):
            self.db.execute("""
                CREATE TABLE keyword_table
                (keyword_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                 name          TEXT COLLATE NOCASE,
                 collection_id INTEGER,
                 doc           TEXT,
                 args          TEXT)
            """)
            self.db.execute("""
                CREATE INDEX keyword_index
                ON keyword_table (name)
            """)


    def _glob_to_sql(self, string):
        """Convert glob-like wildcards to SQL wildcards

        * becomes %
        ? becomes _
        % becomes \%
        \\ remains \\
        \* remains \*
        \? remains \?

        This also adds a leading and trailing %, unless the pattern begins with
        ^ or ends with $
        """

        # What's with the chr(1) and chr(2) nonsense? It's a trick to
        # hide \* and \? from the * and ? substitutions. This trick
        # depends on the substitutiones being done in order.  chr(1)
        # and chr(2) were picked because I know those characters
        # almost certainly won't be in the input string
        table = ((r'\\', chr(1)), (r'\*', chr(2)), (r'\?', chr(3)),
                 (r'%', r'\%'),   (r'?', '_'),     (r'*', '%'),
                 (chr(1), r'\\'), (chr(2), r'\*'), (chr(3), r'\?'))

        for (a, b) in table:
            string = string.replace(a,b)

        string = string[1:] if string.startswith("^") else "%" + string
        string = string[:-1] if string.endswith("$") else string + "%"

        return string

    def _table_exists(self, name):
        cursor = self.db.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='%s'
        """ % name)
        return len(cursor.fetchall()) > 0

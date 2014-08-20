"""Flask blueprint for showing keyword documentation"""

import flask
from flask import current_app
import json

blueprint = flask.Blueprint('doc', __name__,
                            template_folder="templates",
                            static_folder="static")

@blueprint.route("/")
@blueprint.route("/keywords/")
def doc():
    """Show a list of libraries, along with the nav panel on the left"""
    kwdb = current_app.kwdb

    libraries = get_collections(kwdb, libtype="library")
    resource_files = get_collections(kwdb, libtype="resource")
    hierarchy = get_navpanel_data(kwdb)

    return flask.render_template("home.html",
                                 data={"libraries": libraries,
                                       "libdoc": None,
                                       "hierarchy": hierarchy,
                                       "resource_files": resource_files
                                   })


@blueprint.route("/index")
def index():
    """Show a list of available libraries, and resource files"""
    kwdb = current_app.kwdb

    libraries = get_collections(kwdb, libtype="library")
    resource_files = get_collections(kwdb, libtype="resource")

    return flask.render_template("libraryNames.html",
                                 data={"libraries": libraries,
                                       "resource_files": resource_files
                                   })


@blueprint.route("/search/")
def search():
    """Show all keywords that match a pattern"""
    pattern = flask.request.args.get('pattern', "*").strip().lower()

    keywords = []

    for keyword in current_app.kwdb.search(pattern):
        kw = list(keyword)
        url = flask.url_for(".doc_for_library", library=kw[0], keyword=kw[1])
        row_id = "row-%s.%s" % (keyword[0].lower(), keyword[1].lower().replace(" ","-"))
        keywords.append({"collection": keyword[0],
                         "name": keyword[1],
                         "synopsis": keyword[2],
                         "url": url,
                         "row_id": row_id
                     })

    keywords.sort(key=lambda kw: kw["name"])
    return flask.render_template("search.html",
                                 data={"keywords": keywords,
                                       "pattern": pattern
                                   })


# Flask docs imply I can leave the slash off (which I want
# to do for the .../keyword variant). When I do, a URL like
# /doc/BuiltIn/Evaluate gets redirected to the one with a
# trailing slash, which then gives a 404 since the slash
# is invalid. WTF?
@blueprint.route("/keywords/<library>/<keyword>/")
@blueprint.route("/keywords/<library>/")
def doc_for_library(library, keyword=""):
    kwdb = current_app.kwdb

    keywords = []
    for (name, args, doc) in kwdb.get_keyword_data(library):
        # args is a json list; convert it to actual list, and
        # then convert that to a string
        args = ", ".join(json.loads(args))
        doc = doc_to_html(doc)
        target = name == keyword
        keywords.append((name, args, doc, target))

    # this is the introduction documentation for the library
    libdoc = kwdb.get_collection(library)
    libdoc["doc"] = doc_to_html(libdoc["doc"], libdoc["doc_format"])

    # this data is necessary for the nav panel
    hierarchy = get_navpanel_data(kwdb)

    return flask.render_template("library.html",
                                 data={"keywords": keywords,
                                       "libdoc": libdoc,
                                       "hierarchy": hierarchy})

def get_collections(kwdb, libtype="*"):
    """Get list of collections from kwdb, then add urls necessary for hyperlinks"""
    collections = []
    for result in kwdb.get_collections(libtype=libtype):
        url = flask.url_for(".doc_for_library", library=result["name"])
        collections.append((result["name"],url,result["synopsis"]))

    return collections

def get_navpanel_data(kwdb):
    """Get navpanel data from kwdb, and add urls necessary for hyperlinks"""
    data = kwdb.get_keyword_hierarchy()
    for library in data:
        for keyword in library["keywords"]:
            url = flask.url_for(".doc_for_library",
                                library=library["name"],
                                keyword=keyword["name"])
            keyword["url"] = url

    return data


def doc_to_html(doc, doc_format="ROBOT"):
    """Convert documentation to HTML"""
    from robot.libdocpkg.htmlwriter import DocToHtml
    return DocToHtml(doc_format)(doc)

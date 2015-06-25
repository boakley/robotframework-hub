import flask
import argparse
from kwdb import KeywordTable
from flask import current_app
import blueprints
import os
import sys
import robot.errors
from rfhub.version import __version__
import importlib
import inspect
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
import tornado.ioloop
import signal


class RobotHub(object):
    """Robot hub - website for REST and HTTP access to robot files"""
    def __init__(self):

        self.args = self._parse_args()

        if self.args.version:
            print __version__
            sys.exit(0)

        self.kwdb = KeywordTable()
        self.app = flask.Flask(__name__)

        with self.app.app_context():
            current_app.kwdb = self.kwdb

        for lib in self.args.library:
            try:
                self.kwdb.add_library(lib)
            except robot.errors.DataError as e:
                sys.stderr.write("unable to load library '%s'\n" % lib)
                sys.exit(1)

        self._load_keyword_data(self.args.path, self.args.no_installed_keywords)

        self.app.add_url_rule("/", "home", self._root)
        self.app.add_url_rule("/ping", "ping", self._ping)
        self.app.add_url_rule("/favicon.ico", "favicon", self._favicon)
        self.app.register_blueprint(blueprints.api, url_prefix="/api")
        self.app.register_blueprint(blueprints.doc, url_prefix="/doc")
        self.app.register_blueprint(blueprints.dashboard, url_prefix="/dashboard")

    def start(self):
        """Start the app"""
        if self.args.debug:
            self.app.run(port=self.args.port, debug=self.args.debug, host=self.args.interface)
        else:
            root = "http://%s:%s" % (self.args.interface, self.args.port)
            print("tornado web server running on " + root)
            self.shutdown_requested = False
            http_server = HTTPServer(WSGIContainer(self.app))
            http_server.listen(port=self.args.port, address=self.args.interface)

            signal.signal(signal.SIGINT, self.signal_handler)
            tornado.ioloop.PeriodicCallback(self.check_shutdown_flag, 500).start()
            tornado.ioloop.IOLoop.instance().start()

    def signal_handler(self, *args):
        """Handle SIGINT by setting a flag to request shutdown"""
        self.shutdown_requested = True

    def check_shutdown_flag(self):
        """Shutdown the server if the flag has been set"""
        if self.shutdown_requested:
            tornado.ioloop.IOLoop.instance().stop()
            print("web server stopped.")

    def _parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-l", "--library", action="append", default=[],
                            help="load the given LIBRARY (eg: -l DatabaseLibrary)")
        parser.add_argument("-i", "--interface", default="127.0.0.1",
                            help="use the given network interface (default=127.0.0.1)")
        parser.add_argument("-p", "--port", default=7070, type=int,
                            help="run on the given PORT (default=7070)")
        parser.add_argument("-P", "--pythonpath", action=PythonPathAction,
                            help="additional locations to search for libraries.")
        parser.add_argument("--pageobjects", action=PageObjectAction,
                            help="give the name of a module that exports one or more page objects")
        parser.add_argument("-D", "--debug", action="store_true", default=False,
                            help="turn on debug mode")
        parser.add_argument("--no-installed-keywords", action="store_true", default=False,
                            help="do not load some common installed keyword libraries, such as BuiltIn")
        parser.add_argument("--version", action="store_true", default=False,
                            help="Display version number and exit")
        parser.add_argument("path", nargs="*", 
                            help="zero or more paths to folders, libraries or resource files")
        return parser.parse_args()

    def _favicon(self):
        static_dir = os.path.join(self.app.root_path, 'static')
        return flask.send_from_directory(os.path.join(self.app.root_path, 'static'),
                                         'favicon.ico', mimetype='image/vnd.microsoft.icon')

    def _root(self):
        return flask.redirect(flask.url_for('dashboard.home'))

    def _ping(self):
        """This function is called via the /ping url"""
        return "pong"

    def _load_keyword_data(self, paths, no_install_keywords):
        if not no_install_keywords:
            self.kwdb.add_installed_libraries()

        for path in paths:
            try:
                self.kwdb.add(path)
            except Exception as e:
                print "Error adding keywords in %s: %s" % (path, str(e))

class PythonPathAction(argparse.Action):
    """Add a path to PYTHONPATH"""
    def __call__(self, parser, namespace, arg, option_string = None):
        sys.path.insert(0, arg)

class PageObjectAction(argparse.Action):
    '''Handle the -P / --pageobject option

    This finds all pages objects in the given module.  Since page
    objects are libraries, they will be appended to the "library"
    attribute of the namespace and eventually get processed like other
    libraries.

    Note: page object classes that set the class attribute
    '__show_in_rfhub' to False will not be included.

    This works by importing the module given as an argument to the
    option, and then looking for all members of the module that
    inherit from robotpageobjects.Page. 

    For example, if you give the option "pages.MyApp", this will
    attempt to import the module "pages.MyApp", and search for classes
    that are a subclass of Page. For each class it finds it will
    append "pages.MyApp.<class name>" (eg: pages.MyApp.ExamplePage) to
    the list of libraries that will eventually be processed.

    '''

    def __call__(self, parser, namespace, arg, option_string = None):
        from robotpageobjects import Page
        try:
            module = importlib.import_module(name=arg)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Page):
                    # Pay Attention! The attribute we're looking for
                    # takes advantage of name mangling, meaning that
                    # the attribute is unique to the class and won't
                    # be inherited (which is important!). See
                    # https://docs.python.org/2/tutorial/classes.html#private-variables-and-class-local-references

                    attr = "_%s__show_in_rfhub" % obj.__name__
                    if getattr(obj, attr, True):
                        libname = "%s.%s" % (module.__name__, name)
                        namespace.library.append(libname)

        except ImportError:
            print "unable to import '%s'" % arg
            sys.exit(1)

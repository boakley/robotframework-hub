import flask
from argparse import ArgumentParser
from kwdb import KeywordTable
from flask import current_app
import blueprints
import os
import sys
import robot.errors

class RobotHub(object):
    """Robot hub - website for REST and HTTP access to robot files"""
    def __init__(self):

        self.args = self._parse_args()

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
            from tornado.wsgi import WSGIContainer
            from tornado.httpserver import HTTPServer
            from tornado.ioloop import IOLoop
            http_server = HTTPServer(WSGIContainer(self.app))
            http_server.listen(port=self.args.port, address=self.args.interface)
            IOLoop.instance().start()

    def _parse_args(self):
        # N.B. this seems to take < 200ms to load up a
        # decent number of files. I can live with that
        parser = ArgumentParser()
        parser.add_argument("-l", "--library", action="append", default=[],
                            help="load the given LIBRARY (eg: -l DatabaseLibrary)")
        parser.add_argument("-i", "--interface", default="127.0.0.1",
                            help="use the given network interface (default=127.0.0.1)")
        parser.add_argument("-p", "--port", default=7070, type=int,
                            help="run on the given PORT (default=7070)")
        parser.add_argument("-D", "--debug", action="store_true", default=False,
                            help="turn on debug mode")
        parser.add_argument("--no-installed-keywords", action="store_true", default=False,
                            help="do not load some common installed keyword libraries, such as BuiltIn")
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


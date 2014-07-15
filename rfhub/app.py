import flask
from optparse import OptionParser
from kwdb import KeywordTable
from flask import current_app
import blueprints

class RobotHub(object):
    '''Robot hub - website for REST and HTTP access to robot files'''
    def __init__(self):

        # N.B. this seems to take < 200ms to load up a
        # decent number of files. I can live with that
        op = OptionParser()
        op.add_option("-s", "--serve", action="store_true", default=False)
        op.add_option("-p", "--port", default=7070, type="int")
        op.add_option("-D", "--debug", action="store_true", default=False)

        self.opts, args = op.parse_args()

        self.kwdb = KeywordTable()
        self.app = flask.Flask(__name__)

        with self.app.app_context():
            current_app.kwdb = self.kwdb

        self._load_keyword_data(args)

        self.app.add_url_rule("/", "home", self._root)
        self.app.add_url_rule("/ping", "ping", self._ping)
        self.app.register_blueprint(blueprints.api, url_prefix="/api")
        self.app.register_blueprint(blueprints.doc, url_prefix="/doc")
        self.app.register_blueprint(blueprints.dashboard, url_prefix="/dashboard")

    def start(self):
        '''Start the app'''
        self.app.run(port=self.opts.port, debug=self.opts.debug)

    def _root(self):
        return flask.redirect(flask.url_for('dashboard.home'))
        
    def _ping(self):
        '''This function is called via the /ping url'''
        return "pong"

    def _load_keyword_data(self, args):
        self.kwdb.add_installed_libraries()

        for path in args:
            try:
                self.kwdb.add(path)
            except Exception as e:
                print "Error adding keywords in %s: %s" % (path, str(e))

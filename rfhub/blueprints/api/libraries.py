'''
This provides the view functions for the /api/libraries endpoints
'''

import flask
from flask import current_app

class ApiEndpoint(object):
    def __init__(self, blueprint):
        blueprint.add_url_rule("/libraries/", view_func = self.get_libraries)
        blueprint.add_url_rule("/libraries/<library>", view_func = self.get_library)
        
    def get_libraries(self):
        kwdb = current_app.kwdb

        query_pattern = flask.request.args.get('pattern', "*").strip().lower()
        libraries = kwdb.get_collections(query_pattern)

        return flask.jsonify(libraries=libraries)

    def get_library(self, library):
        kwdb = current_app.kwdb
        library = kwdb.get_collection(library)
        return flask.jsonify(library=library)

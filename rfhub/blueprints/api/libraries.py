'''
This provides the view functions for the /api/libraries endpoints
'''

import flask
from flask import current_app

class ApiEndpoint(object):
    def __init__(self, blueprint):
        blueprint.add_url_rule("/libraries/", view_func = self.get_libraries)
        blueprint.add_url_rule("/libraries/<collection_id>", view_func = self.get_library)
        
    def get_libraries(self):
        kwdb = current_app.kwdb

        query_pattern = flask.request.args.get('pattern', "*").strip().lower()
        libraries = kwdb.get_collections(query_pattern)

        return flask.jsonify(libraries=libraries)

    def get_library(self, collection_id):
        # if collection_id is a library _name_, redirect
        print "get_library: collection_id=", collection_id
        kwdb = current_app.kwdb
        collection = kwdb.get_collection(collection_id)
        return flask.jsonify(collection=collection)

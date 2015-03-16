'''
This provides the view functions for the /api/keywords endpoints
'''

import flask
from flask import current_app
from robot.libdocpkg.htmlwriter import DocToHtml

class ApiEndpoint(object):
    def __init__(self, blueprint):
        blueprint.add_url_rule("/keywords/", view_func = self.get_keywords)
        blueprint.add_url_rule("/keywords/<collection_id>", view_func = self.get_library_keywords)
        blueprint.add_url_rule("/keywords/<collection_id>/<keyword>", view_func = self.get_library_keyword)
        
    def get_library_keywords(self,collection_id):

        query_pattern = flask.request.args.get('pattern', "*").strip().lower()
        keywords = current_app.kwdb.get_keywords(query_pattern)

        req_fields  = flask.request.args.get('fields', "*").strip().lower()
        if (req_fields == "*"):
            fields = ("collection_id","library", "name","synopsis","doc","htmldoc","args",
                      "doc_keyword_url", "api_keyword_url", "api_library_url")
        else:
            fields = [x.strip() for x in req_fields.split(",")]

        result = []
        for (keyword_collection_id, keyword_collection_name,
             keyword_name, keyword_doc, keyword_args) in keywords:
            if collection_id == "" or collection_id == keyword_collection_id:
                data = {}
                if ("collection_id" in fields): data["collection_id"] = keyword_collection_id
                if ("library" in fields): data["library"] = keyword_collection_name
                if ("name" in fields): data["name"] = keyword_name
                if ("synopsis" in fields): data["synopsis"] = keyword_doc.strip().split("\n")[0]
                if ("doc" in fields): data["doc"] = keyword_doc
                if ("args" in fields): data["args"] = keyword_args

                if ("doc_keyword_url" in fields): 
                    data["doc_keyword_url"] = flask.url_for("doc.doc_for_library",
                                                            collection_id=keyword_collection_id,
                                                            keyword=keyword_name)
                if ("api_keyword_url" in fields):
                    data["api_keyword_url"] = flask.url_for(".get_library_keyword", 
                                                            collection_id=keyword_collection_id,
                                                            keyword=keyword_name)

                if ("api_library_url" in fields):
                    data["api_library_url"] = flask.url_for(".get_library_keywords",
                                                            collection_id=keyword_collection_id)
                if ("htmldoc" in fields):
                    try:
                        data["htmldoc"] = DocToHtml("ROBOT")(keyword_doc)
                    except Exception, e:
                        data["htmldoc"] = "";
                        htmldoc = "bummer", e


                result.append(data)

        return flask.jsonify(keywords=result)

    def get_keywords(self):
        # caller wants a list of keywords
        collection_id = flask.request.args.get('collection_id', "")
        return self.get_library_keywords(collection_id)

    def get_library_keyword(self, collection_id, keyword):
        kwdb = current_app.kwdb

        # if collection_id is a name, redirect?
        collections = kwdb.get_collections(pattern=collection_id.strip().lower())
        if len(collections) == 1:
            collection_id = collections[0]["collection_id"]
        else:
            # need to redirect to a disambiguation page
            flask.abort(404)
        
        try:
            keyword = kwdb.get_keyword(collection_id, keyword)

        except Exception, e:
            current_app.logger.warning(e)
            flask.abort(404)

        if keyword:
            lib_url = flask.url_for(".get_library", collection_id=keyword["collection_id"])
            keyword["library_url"] = lib_url
            return flask.jsonify(keyword)
        else:
            flask.abort(404)



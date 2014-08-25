'''
API blueprint

This blueprint provides the /api interface.

'''

import flask
from flask import current_app
from robot.libdocpkg.htmlwriter import DocToHtml

blueprint = flask.Blueprint('api', __name__)

@blueprint.route("/keywords/")
def get_keywords():

    # caller wants a list of keywords
    lib = flask.request.args.get('library', "").strip().lower()
    return get_library_keywords(lib)

@blueprint.route("/keywords/<library>")
def get_library_keywords(library):

    query_pattern = flask.request.args.get('pattern', "*").strip().lower()
    keywords = current_app.kwdb.get_keywords(query_pattern)
    library = library.strip().lower()

    req_fields  = flask.request.args.get('fields', "*").strip().lower()
    if (req_fields == "*"):
        fields = ("library","name","synopsis","doc","htmldoc","args",
                  "doc_keyword_url", "api_keyword_url", "api_library_url")
    else:
        fields = [x.strip() for x in req_fields.split(",")]

    result = []
    for (keyword_library, keyword_name, keyword_doc, keyword_args) in keywords:
        if library == "" or library == keyword_library.strip().lower():
            data = {}
            if ("library" in fields): data["library"] = keyword_library
            if ("name" in fields): data["name"] = keyword_name
            if ("synopsis" in fields): data["synopsis"] = keyword_doc.strip().split("\n")[0]
            if ("doc" in fields): data["doc"] = keyword_doc
            if ("args" in fields): data["args"] = keyword_args

            if ("doc_keyword_url" in fields): 
                data["doc_keyword_url"] = flask.url_for("doc.doc_for_library",
                                                        library=keyword_library,
                                                        keyword=keyword_name)
            if ("api_keyword_url" in fields):
                data["api_keyword_url"] = flask.url_for(".get_library_keyword", 
                                                        library=keyword_library, 
                                                        keyword=keyword_name)
                
            if ("api_library_url" in fields):
                data["api_library_url"] = flask.url_for(".get_library_keywords",
                                                        library=keyword_library)
            print "trying to get htmldoc?", ("htmldoc" in fields)
            if ("htmldoc" in fields):
                try:
                    data["htmldoc"] = DocToHtml("ROBOT")(keyword_doc)
                except Exception, e:
                    data["htmldoc"] = "";
                    htmldoc = "bummer", e
                    
 
            result.append(data)

    return flask.jsonify(keywords=result)

@blueprint.route("/keywords/<library>/<keyword>")
def get_library_keyword(library, keyword):
    kwdb = current_app.kwdb
    try:
        keyword = kwdb.get_keyword(library, keyword)
    except Exception, e:
        current_app.logger.warning(e)
        flask.abort(404)

    if keyword:
        lib_url = flask.url_for(".get_library", library=keyword["library"])
        keyword["library_url"] = lib_url
        return flask.jsonify(keyword)
    else:
        flask.abort(404)

@blueprint.route("/libraries/")
def get_libraries():
    kwdb = current_app.kwdb

    query_pattern = flask.request.args.get('pattern', "*").strip().lower()
    libraries = kwdb.get_collections(query_pattern)

    return flask.jsonify(libraries=libraries)

@blueprint.route("/libraries/<library>")
def get_library(library):
    kwdb = current_app.kwdb
    library = kwdb.get_collection(library)
    return flask.jsonify(library=library)


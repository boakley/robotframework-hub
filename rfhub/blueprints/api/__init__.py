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

    kwdb = current_app.kwdb
    query_pattern = flask.request.args.get('pattern', "*").strip().lower()
    keywords = kwdb.get_keywords(query_pattern)
    result = []
    library = library.strip().lower()
    for (keyword_library, keyword_name, keyword_doc, keyword_args) in keywords:
        if library == "" or library == keyword_library.strip().lower():
            api_kw_url = flask.url_for(".get_library_keyword", 
                                       library=keyword_library, 
                                       keyword=keyword_name)
            api_lib_url = flask.url_for(".get_library_keywords",
                                        library=keyword_library)
            try:
                htmldoc = DocToHtml("ROBOT")(keyword_doc)
            except Exception, e:
                htmldoc = "bummer"

            result.append({"library": keyword_library, 
                           "name": keyword_name, 
                           "synopsis": keyword_doc.strip().split("\n")[0],
                           "doc": keyword_doc,
                           "htmldoc": htmldoc,
                           "args": keyword_args,
                           "api_keyword_url": api_kw_url,
                           "api_library_url": api_lib_url})
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



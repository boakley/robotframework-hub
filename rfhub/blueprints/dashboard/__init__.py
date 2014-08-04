import flask
from flask import current_app

blueprint = flask.Blueprint('dashboard', __name__,
                            template_folder="templates")

@blueprint.route("/")
def home():
    
    return flask.render_template("dashboard.html")



    

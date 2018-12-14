from flask import Blueprint, render_template


ml_blueprint = Blueprint('ml', __name__, template_folder='templates')

@ml_blueprint.route("/teaching")
@ml_blueprint.route("/teaching/")
def teaching():
    return render_template('teaching.html')

@ml_blueprint.route("/projects")
@ml_blueprint.route("/projects/")
def projects():
    return render_template('projects.html')
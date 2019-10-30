from flask import Blueprint, render_template
from application.models import *

ml_blueprint = Blueprint('ml', __name__, template_folder='templates')

@ml_blueprint.route("/teaching")
@ml_blueprint.route("/teaching/")
def teaching():
    data = StaticPage.query.filter(StaticPage.route == "teaching").one_or_none()
    return render_template('teaching.html', data=data)

@ml_blueprint.route("/projects")
@ml_blueprint.route("/projects/")
def projects():
    data = StaticPage.query.filter(StaticPage.route == "projects").one_or_none()
    return render_template('projects.html', data=data)

@ml_blueprint.route("/workshops")
@ml_blueprint.route("/workshops/")
def projects():
    data = StaticPage.query.filter(StaticPage.route == "workshops").one_or_none()
    return render_template('workshops.html', data=data)
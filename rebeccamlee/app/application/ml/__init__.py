from flask import Blueprint, render_template
from application.models import *

ml_blueprint = Blueprint('ml', __name__, template_folder='templates')

@ml_blueprint.route("/teaching")
@ml_blueprint.route("/teaching/")
def teaching():
    data = StaticPage.query.filter(StaticPage.route == "teaching").one_or_none()
    return render_template('teaching.html', data=data)

@ml_blueprint.route("/portfolio")
@ml_blueprint.route("/portfolio/")
def portfolio():
    data = StaticPage.query.filter(StaticPage.route == "portfolio").one_or_none()
    return render_template('portfolio.html', data=data)

@ml_blueprint.route("/resume")
@ml_blueprint.route("/resume/")
def resume():
    data = StaticPage.query.filter(StaticPage.route == "resume").one_or_none()
    return render_template('resume.html', data=data)
from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_user
from config import ASANA_CODE, ASANA_PROJECT_ID
import requests, json, datetime
from application.models import *
from application import db

timeline_blueprint = Blueprint('timeline', __name__, template_folder='templates')

#helper function for decorator to pass global info to templates
def generate_site_data():
    basics = Basics.query.first()
    return basics

#app context processor for sitewide data. Use as a decorator @include_site_data after @app.route to include a variable called basics in rendered template
def include_site_data(fn):
    @timeline_blueprint.context_processor
    def additional_context():
        #site_basics
        basics = generate_site_data()

        return {"basics":basics}
    return fn

@timeline_blueprint.route("/timeline")
@timeline_blueprint.route("/timeline/")
@timeline_blueprint.route("/timeline/<entry_id>")
@timeline_blueprint.route("/timeline/<entry_id>/")
@include_site_data
def timeline(entry_id=None):
    if entry_id:
        timeline_entry= TimelineEntry.query.filter(TimelineEntry.id == entry_id).one_or_none()
        return render_template("timeline_row.html", timeline_entry=timeline_entry)
    else:
        return render_template("timeline.html")

@timeline_blueprint.route("/timelinedata")
@include_site_data
def timelinedata():
    timeline_rows = TimelineEntry.query.all()
    return render_template("timelinedata.json", timeline_rows=timeline_rows)
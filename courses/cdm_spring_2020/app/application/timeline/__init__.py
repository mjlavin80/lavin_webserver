from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user, login_user
from config import ASANA_CODE, ASANA_PROJECT_ID
import requests, json, datetime
from application.models import *
from application import db

timeline_blueprint = Blueprint('timeline', __name__, template_folder='templates')

@timeline_blueprint.route("/timeline")
@timeline_blueprint.route("/timeline/")
@timeline_blueprint.route("/timeline/<entry_id>")
@timeline_blueprint.route("/timeline/<entry_id>/")
def timeline(entry_id=None):
    if entry_id:
        timeline_entry= TimelineEntry.query.filter(TimelineEntry.id == entry_id).one_or_none()
        return render_template("timeline_row.html", timeline_entry=timeline_entry)
    else:
        return render_template("timeline.html")

@timeline_blueprint.route("/timelinedata")
def timelinedata():
    timeline_rows = TimelineEntry.query.all()
    return render_template("timelinedata.json", timeline_rows=timeline_rows)
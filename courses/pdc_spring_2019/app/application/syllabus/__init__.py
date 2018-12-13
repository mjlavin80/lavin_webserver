from flask import Blueprint, render_template
from application.models import Basics, Policy, Assignment, Reading, Activity, Day, Week
from sqlalchemy.sql import and_

syllabus_blueprint = Blueprint('syllabus', __name__, template_folder='templates')

@syllabus_blueprint.route("/policies")
def policies():
    policies = Policy.query.filter(Policy.public == "True").all()
    return render_template("policies.html", policies=policies)

@syllabus_blueprint.route("/calendar")
def calendar():
    #get weeks from db
    weeks = Week.query.order_by(Week.week_number).all()
    return render_template("calendar.html", weeks=weeks)

@syllabus_blueprint.route("/assignments/<this_assignment>")
@syllabus_blueprint.route("/assignments")
def assignments(this_assignment="all"):
    if this_assignment != "all":
        #get assignment from db
        try:
            a = Assignment.query.filter(and_(Assignment.link_title == this_assignment, Assignment.public == "True")).one_or_none()
            if a == []:
                return redirect(url_for("assignments", assignments=[], this_assignment="all"))
            return render_template("assignments.html", assignments=[], this_assignment=a)
        except:
            return redirect(url_for("assignments", assignments=[], this_assignment="all"))
    else:
        a = Assignment.query.all()
        return render_template("assignments.html", assignments=a, this_assignment="all")

@syllabus_blueprint.route("/activities/<this_activity>")
@syllabus_blueprint.route("/activities")
def activities(this_activity="all"):
    if this_activity != "all":
        #get activity from db
        a = Activity.query.filter(Activity.id == this_activity).one_or_none()
        if a:
            return render_template("activities.html", activities=[], this_activity=a)
        else:
            a = Activity.query.filter(Activity.public == "True").all()
            a.sort(key=lambda x: x.day.id)
            return render_template("activities.html", activities=a, this_activity="all")
    else:
        a = Activity.query.filter(Activity.public == "True").all()
        a.sort(key=lambda x: x.day.id)
        return render_template("activities.html", activities=a, this_activity="all")

@syllabus_blueprint.route("/readings")
def readings():
    try:
        days = Day.query.all()
        readings = []
        for d in days:
            for r in d.readings:
                readings.append(r)
    except:
        readings = []
    return render_template("readings.html", readings=readings)

@syllabus_blueprint.route('/coming_soon')
def coming_soon():
    return render_template("soon.html")

@syllabus_blueprint.route("/required_book")
def required_book():
    book_policy = Policy.query.filter(and_(Policy.public == "True", Policy.title =="Required Texts")).all()
    return render_template("required_book.html", book_policy=book_policy)

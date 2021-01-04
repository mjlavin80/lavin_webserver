from flask import Blueprint, redirect, url_for, render_template
from application.models import StaticPage, Syllabus
from application import db

courses_blueprint = Blueprint("courses", __name__, template_folder="templates")

@courses_blueprint.route("/courses")
def courses():
    data = StaticPage.query.filter(StaticPage.route == "courses").one_or_none()
    return render_template("main.html", data=data)

@courses_blueprint.route("/da-101")
@courses_blueprint.route("/da-101/<semester>")
def da_101(semester=None):
    if not semester:
        # this doesn't work because I might be working on syllabus for next term
        # latest_term = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-101").all()
        # latest_term = [i.semester.replace('spring','0').replace('fall', '1') for i in latest_term]
        # latest_tuple = [i.split('-') for i in latest_term]
        # latest_tuple = [(int(i[0]), int(i[1])) for i in latest_tuple]
        # latest_tuple = sorted(latest_tuple, key = lambda x: (-x[1],-x[0]))
        # latest = str(latest_tuple[0][0]).replace('0', 'spring').replace('1','fall') + "-" + str(latest_tuple[0][1])
        return redirect(url_for("courses.da_101", semester="spring-2021"))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-101").filter(Syllabus.semester == semester).one_or_none()
    
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 101", course_name="Introduction to Data Analytics")

@courses_blueprint.route("/da-301")
@courses_blueprint.route("/da-301/<semester>")
def da_301(semester=None):
    if not semester:
        return redirect(url_for("courses.da_301", semester="fall-2020"))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-301").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 301", course_name="Practicum in Data Analytics")

@courses_blueprint.route("/da-401")
@courses_blueprint.route("/da-401/<semester>")
def da_401(semester=None):
    if not semester:
        return redirect(url_for("courses.da_401", semester="spring-2021"))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-401").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 401", course_name="Seminar in Data Analytics")

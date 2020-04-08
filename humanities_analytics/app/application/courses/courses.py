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
        return redirect(url_for("courses.da_101", semester="fall-2020"))
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

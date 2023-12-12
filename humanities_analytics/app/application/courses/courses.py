from flask import Blueprint, redirect, url_for, render_template
from application.models import StaticPage, Syllabus
from application import db

courses_blueprint = Blueprint("courses", __name__, template_folder="templates")

@courses_blueprint.route("/courses")
def courses():
    data = StaticPage.query.filter(StaticPage.route == "courses").one_or_none()
    return render_template("main.html", data=data)

def load_course(semester=None, course=None, template=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == course).one_or_none()
        return redirect(url_for("courses." + course.replace("-", "_"), semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    cn= course.replace("-", " ").capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == course).filter(Syllabus.semester == semester).one_or_none()
    return render_template(template, syllabus=syllabus, term_string=term_string, course_number=cn, course_name=syllabus.course_name)

@courses_blueprint.route("/da-101")
@courses_blueprint.route("/da-101/")
@courses_blueprint.route("/da-101/<semester>")
@courses_blueprint.route("/da-101/<semester>/")
def da_101(semester=None, course="da-101", template="lab_syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-200")
@courses_blueprint.route("/da-200/")
@courses_blueprint.route("/da-200/<semester>")
@courses_blueprint.route("/da-200/<semester>/")
def da_200(semester=None, course="da-200", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-210")
@courses_blueprint.route("/da-210/")
@courses_blueprint.route("/da-210/<semester>")
@courses_blueprint.route("/da-210/<semester>/")
def da_210(semester=None, course="da-210", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-245")
@courses_blueprint.route("/da-245/")
@courses_blueprint.route("/da-245/<semester>")
@courses_blueprint.route("/da-245/<semester>/")
def da_245(semester=None, course="da-245", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-301")
@courses_blueprint.route("/da-301/")
@courses_blueprint.route("/da-301/<semester>")
@courses_blueprint.route("/da-301/<semester>/")
def da_301(semester=None, course="da-301", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-350")
@courses_blueprint.route("/da-350/")
@courses_blueprint.route("/da-350/<semester>")
@courses_blueprint.route("/da-350/<semester>/")
def da_350(semester=None, course="da-350", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-351")
@courses_blueprint.route("/da-351/")
@courses_blueprint.route("/da-351/<semester>")
@courses_blueprint.route("/da-351/<semester>/")
def da_351(semester=None, course="da-351", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

@courses_blueprint.route("/da-401")
@courses_blueprint.route("/da-401/")
@courses_blueprint.route("/da-401/<semester>")
@courses_blueprint.route("/da-401/<semester>/")
def da_401(semester=None, course="da-401", template="syllabus.html"):
    return load_course(semester=semester, course=course, template=template)

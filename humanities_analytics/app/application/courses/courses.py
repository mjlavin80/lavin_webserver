from flask import Blueprint, redirect, url_for, render_template
from application.models import StaticPage, Syllabus
from application import db

courses_blueprint = Blueprint("courses", __name__, template_folder="templates")

@courses_blueprint.route("/courses")
def courses():
    data = StaticPage.query.filter(StaticPage.route == "courses").one_or_none()
    return render_template("main.html", data=data)

@courses_blueprint.route("/da-101")
@courses_blueprint.route("/da-101/")
@courses_blueprint.route("/da-101/<semester>")
@courses_blueprint.route("/da-101/<semester>/")
def da_101(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-101").one_or_none()
        return redirect(url_for("courses.da_101", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-101").filter(Syllabus.semester == semester).one_or_none()
    return render_template("lab_syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 101", course_name=syllabus.course_name)

@courses_blueprint.route("/da-200")
@courses_blueprint.route("/da-200/")
@courses_blueprint.route("/da-200/<semester>")
@courses_blueprint.route("/da-200/<semester>/")
def da_200(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-200").one_or_none()
        return redirect(url_for("courses.da_200", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-200").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 200", course_name=syllabus.course_name)

def load_course(semester=None, course=None, template=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == course).one_or_none()
        return redirect(url_for("courses." + course.replace("-", "_"), semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    cn= course.replace("-", " ").capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == course).filter(Syllabus.semester == semester).one_or_none()
    return render_template(template, syllabus=syllabus, term_string=term_string, course_number=cn, course_name=syllabus.course_name)

@courses_blueprint.route("/da-210")
@courses_blueprint.route("/da-210/")
@courses_blueprint.route("/da-210/<semester>")
@courses_blueprint.route("/da-210/<semester>/")
def da_210(semester=None, course=None, template=None):
    return load_course(semester=None, course="da-210", template="syllabus.html")

@courses_blueprint.route("/da-245")
@courses_blueprint.route("/da-245/")
@courses_blueprint.route("/da-245/<semester>")
@courses_blueprint.route("/da-245/<semester>/")
def da_245(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-200").one_or_none()
        return redirect(url_for("courses.da_245", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-245").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 245", course_name=syllabus.course_name)

@courses_blueprint.route("/da-301")
@courses_blueprint.route("/da-301/")
@courses_blueprint.route("/da-301/<semester>")
@courses_blueprint.route("/da-301/<semester>/")
def da_301(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-301").one_or_none()
        return redirect(url_for("courses.da_301", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-301").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 301", course_name=syllabus.course_name)

@courses_blueprint.route("/da-350")
@courses_blueprint.route("/da-350/")
@courses_blueprint.route("/da-350/<semester>")
@courses_blueprint.route("/da-350/<semester>/")
def da_350(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-350").one_or_none()
        return redirect(url_for("courses.da_350", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-350").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 350", course_name=syllabus.course_name)

@courses_blueprint.route("/da-351")
@courses_blueprint.route("/da-351/")
@courses_blueprint.route("/da-351/<semester>")
@courses_blueprint.route("/da-351/<semester>/")
def da_351(semester=None, course=None, template=None):
    return load_course(semester=None, course="da-351", template="syllabus.html")
    
@courses_blueprint.route("/da-401")
@courses_blueprint.route("/da-401/")
@courses_blueprint.route("/da-401/<semester>")
@courses_blueprint.route("/da-401/<semester>/")
def da_401(semester=None):
    if not semester:
        current = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.current=='True').filter(Syllabus.course == "da-401").one_or_none()
        return redirect(url_for("courses.da_401", semester=current.semester))
    term_string = " ".join(semester.split("-")).capitalize()
    syllabus = db.session.query(Syllabus).filter(Syllabus.public=='True').filter(Syllabus.course == "da-401").filter(Syllabus.semester == semester).one_or_none()
    return render_template("syllabus.html", syllabus=syllabus, term_string=term_string, course_number="DA 401", course_name=syllabus.course_name)

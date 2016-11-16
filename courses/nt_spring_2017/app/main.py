from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from application.models import *
from application import db
from flask_login import login_required
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')

admin = Admin(app, name='Dashboard', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Reading, db.session))
admin.add_view(ModelView(Assignment, db.session))
admin.add_view(ModelView(Day, db.session))
admin.add_view(ModelView(Week, db.session))
admin.add_view(ModelView(Basics, db.session))

#helper function for decorator to pass global info to templates
def generate_site_data():
    basics = Basics.query.one_or_none()
    return basics

#app context processor for sitewide data. Use as a decorator @include_site_data after @app.route to include a variable called basics in rendered template
def include_site_data(fn):
    @app.context_processor
    def additional_context():
        basics = generate_site_data()
        return {"basics":basics}
    return fn

#Begin route declarations
@app.route("/")
@include_site_data
def index():
     return render_template("index.html")

@app.route("/policies")
@include_site_data
def policies():
    return render_template("policies.html")

@app.route("/calendar")
@include_site_data
def calendar():
    #get weeks from db
    weeks = Week.query.all()
    return render_template("calendar.html", weeks=weeks)

@app.route("/assignments/<this_assignment>")
@app.route("/assignments")
@include_site_data
def assignments(this_assignment="all"):
    if this_assignment != "all":
        #get assignment from db
        try:
            a = Assignment.query.filter(Assignment.link_title == this_assignment).one_or_none()
            if a == []:
                return redirect(url_for("assignments", assignments=[], this_assignment="all"))
            return render_template("assignments.html", assignments=[], this_assignment=a)
        except:
            return redirect(url_for("assignments", assignments=[], this_assignment="all"))
    else:
        a = Assignment.query.all()
        return render_template("assignments.html", assignments=a, this_assignment="all")

@app.route("/readings")
@include_site_data
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

@app.route("/bibliography")
@include_site_data
def biblio():
    #get items from Zotero
    return render_template("bibliography.html")

@app.route('/protected/<path:filename>')
@include_site_data
#login_required
def protected(filename):
    path = os.path.join(app.instance_path, 'protected')
    return send_from_directory(path, filename)

@app.route('/coming_soon')
@include_site_data
def coming_soon():
    return render_template("soon.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    #for production
    #app.run(host='0.0.0.0', port=port)

    #for dev
    app.run(host='0.0.0.0', debug=True, port=5000)

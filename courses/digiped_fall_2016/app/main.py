from flask import Flask, render_template, redirect, url_for, send_from_directory
import os
#from application.models import *
#from application import db
#from flask_login import login_required

app = Flask(__name__)

@app.route("/")
def index():
     return render_template("index.html")

@app.route("/policies")
def policies():
    return render_template("policies.html")

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/assignments/<assignment>")
@app.route("/assignments")
def assignments(assignment="all"):
    assign_dict = {"all": "all_assignments.html", "teaching_philosophy": "philo.html", "skills_proposal": "proposal.html", "skills_assignment": "skills.html", "lesson_plan": "lesson.html", "seminar_paper": "seminar.html"}
    try:
        assign_text = assign_dict[assignment]
    except:
        return redirect(url_for('assignments', assignment="all"))
    return render_template("assignments.html", assign_text=assign_text)

@app.route("/readings")
def readings():
    return render_template("readings.html")

@app.route("/bibliography")
def biblio():
    return render_template("bibliography.html")

@app.route('/protected/<path:filename>')
#login_required
def protected(filename):
    path = os.path.join(app.instance_path, 'protected')
    return send_from_directory(path, filename)

@app.route('/coming_soon')
#login_required
def soon():
    return render_template("soon.html")

#this section needs a layer of protection so a user can't reset the db
#@app.route("/setup")
#def setup():
#    try:
#        db.create_all()
#        return "DB successfully set up."
#    except:
#        return "Database already set up. No action needed."

if __name__ == "__main__":
    #for local dev
    #app.run(host='0.0.0.0', debug=True)

    #for production
    app.run(host='0.0.0.0', port=80)

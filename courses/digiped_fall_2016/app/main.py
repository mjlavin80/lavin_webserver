from flask import Flask, render_template, redirect
import os
from application.models import *
from application import db

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

@app.route("/assignments")
def assignments():
    return render_template("assignments.html")

@app.route("/readings")
def readings():
    return render_template("readings.html")

@app.route("/bibliography")
def biblio():
    return render_template("bibliography.html")

#this section needs a layer of protection so a user can't reset the db
"""
@app.route("/setup")
def setup():
    try:
        db.create_all()
        return "DB successfully set up."
    except:
        return "Database already set up. No action needed."
"""

if __name__ == "__main__":
    #for local dev
    #app.run(host='0.0.0.0', debug=True)

    #for production
    app.run(host='0.0.0.0', port=80)

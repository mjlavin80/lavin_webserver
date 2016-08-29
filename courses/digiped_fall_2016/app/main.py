from flask import Flask
import os
from application.models import *
from application import db

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World from Flask"

#this section needs a layer of protection so a user can't resest the db
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

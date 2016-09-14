from flask import Flask, render_template, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def index():
     return "Hello world from Fasl app2"


if __name__ == "__main__":
    #for local dev
    #app.run(host='0.0.0.0', debug=True)

    #for production
    app.run(host='0.0.0.0', port=8080)

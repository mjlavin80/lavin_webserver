from flask import Flask, render_template, request, redirect, url_for, flash, abort
from application.genres import make_genres_big_and_lavin
from config import *
from datetime import datetime
import json
import sqlite3
import pickle

app = Flask(__name__)

app.secret_key = SECRET_KEY

metadata = pickle.load( open( "metadata.p", "rb" ) )

piped_genres = [i[14] for i in metadata]
processed_genres, big_genres, lavin_genres = make_genres_big_and_lavin(piped_genres)

metadata_dict = {}
for h,i in enumerate(metadata):
    metadata_dict[i[0]] = i[1:15]
    metadata_dict[i[0]].append(big_genres[h])

@app.route("/", methods=["GET", "POST"])
@app.route("/<doc_id>", methods=["GET", "POST"])
def index(doc_id=None):
    if doc_id:
        conn = sqlite3.connect('regression_scores.db')
        c = conn.cursor()
        query = """SELECT margin FROM results WHERE doc_id=?"""
        data = c.execute(query, (doc_id,)).fetchall()


        if len(data) == 0:
            return redirect(url_for("index", doc_id=None))
        else:
            meta = metadata_dict[doc_id]
            columns = ["recordid", "oclc", "locnum", "author", "imprint", "date", "birthdate", "firstpub", "enumcron", "subjects",
            "title", "nationality", "gender", "genretags", "final_genre"]
            meta_dict = {}
            for j,k in enumerate(columns):
                meta_dict[k] = meta[j]

            return render_template("doc.html", doc_id=doc_id, meta_dict=meta_dict)
    else:
        return render_template("index.html", doc_id=doc_id)

@app.route("/train_ids/<doc_id>/test/<test_number>", methods=["GET", "POST"])
def test_ids(doc_id=None, test_number=None):
    conn = sqlite3.connect('regression_scores.db')
    c = conn.cursor()
    query = "SELECT main.train_ids FROM results LEFT JOIN main on main.id = results.main_id WHERE doc_id=?"
    all_data = [i[0] for i in c.execute(query, (doc_id,)).fetchall()]
    data = all_data[int(test_number)].split(", ")
    return render_template('train_ids.html', data=data, doc_id=doc_id, test_number=test_number)

@app.route("/data", methods=["GET", "POST"])
@app.route("/data/<doc_id>", methods=["GET", "POST"])
def data(doc_id=None):
    if doc_id:
        conn = sqlite3.connect('regression_scores.db')
        c = conn.cursor()
        query = """SELECT predicted, actual, margin FROM results WHERE doc_id=?"""
        data = c.execute(query, (doc_id,)).fetchall()
        if len(data) == 0:
            return redirect("static/dist/js/data.js")
        else:
            #convert data to json
            headers = ["predicted", "actual", "margin", "train_ids"]
            data_dicts = []
            for h, i in enumerate(data):
                d_dict = {}
                d_dict["train_ids"] = "<a href='../train_ids/"+doc_id+"/test/"+str(h)+"' data-toggle='lightbox' title='test IDs'>Click to View</a>"
                for j, k in enumerate(i):
                    d_dict[headers[j]] = str(k)

                data_dicts.append(d_dict)
            result = json.dumps(data_dicts)
        return result
    else:
        return redirect("static/dist/js/data.js")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(502)
def gateway_error(e):
    return render_template('500.html'), 502

if __name__ == "__main__":
    #for local dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    app.run(host='0.0.0.0', debug=True, port=80)

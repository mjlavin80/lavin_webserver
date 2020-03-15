from flask import Blueprint, render_template, request, redirect, url_for
from application.models import *
from flask_login import current_user
from  sqlalchemy.sql.expression import func
import datetime

data_blueprint = Blueprint('data', __name__, template_folder='templates')

@data_blueprint.route("/")
@data_blueprint.route("/<aps_id>")
@data_blueprint.route("/<aps_id>/")
def index(aps_id=None):
    if not current_user.is_authenticated or not current_user.approved:
        return render_template("index.html", aps_id=None)
    else:
        if aps_id:
            row = Review().query.filter(Review.record_id == aps_id).one_or_none()

            return render_template("index.html", aps_id=aps_id, row=row)
        
        else:
        	#change to rand() for mysql
            row = Review().query.filter(Review.status == 'needs_audit').order_by(func.random()).first()
            try:
            	aps_id = row.record_id
            except: 
            	aps_id = ""
            return render_template("index.html", aps_id=aps_id, row=row)

@data_blueprint.route("/crosscheck")
@data_blueprint.route("/crosscheck/<aps_id>")
@data_blueprint.route("/crosscheck/<aps_id>/")
def crosscheck(aps_id=None):
    if not current_user.is_authenticated or not current_user.approved:
        return render_template("index.html", aps_id=None)
    else:
        if aps_id:
            row = Review().query.filter(Review.record_id == aps_id).one_or_none()
            if row.user_id == current_user.id:
                return render_template("crosscheck.html", aps_id=None)
            
            return render_template("crosscheck.html", aps_id=aps_id, row=row)
        else:
            
            row = Review().query.filter(Review.status == 'needs_crosscheck').filter(Review.user_id != current_user.id).order_by(func.random()).first()
            try:
                aps_id = row.record_id
            except: 
                aps_id = ""
            return render_template("crosscheck.html", aps_id=aps_id, row=row)

@data_blueprint.route("/add_crosscheck", methods=["GET", "POST"])
@data_blueprint.route("/add_crosscheck/<aps_id>", methods=["GET", "POST"])
@data_blueprint.route("/add_crosscheck/<aps_id>/", methods=["GET", "POST"])
def add_crosscheck(aps_id=None): 
    if aps_id:
        if request.method == 'POST':
            meta = Review().query.filter(Review.record_id == aps_id).one_or_none()
            meta.status = 'done'
            db.session.commit()
            
            crosscheck = ExtractedParsed()
            
            crosscheck.review_id = meta.id
            crosscheck.experiment = "crosscheck "
            crosscheck.annotation = str(current_user.id)
            crosscheck.date_time = datetime.date.today().strftime("%Y-%m-%d")
            
            for key in request.form.keys():
                if key != "perceived_author_gender":
                    setattr(crosscheck, key, request.form[key])
                else:   
                    if request.form[key] != 'na':
                        crosscheck.perceived_author_gender = request.form[key]
            
            db.session.add(crosscheck)
            db.session.commit()

            return render_template("cross_success.html", aps_id=aps_id) 
            
    else:
        return(redirect(url_for('data.index')))


@data_blueprint.route("/update", methods=["GET", "POST"])
@data_blueprint.route("/update/<aps_id>", methods=["GET", "POST"])
@data_blueprint.route("/update/<aps_id>/", methods=["GET", "POST"])
def update(aps_id=None): 
    if aps_id:
        if request.method == 'POST':
            meta = Review().query.filter(Review.record_id == aps_id).one_or_none()
            for key in request.form.keys():
                if key != "perceived_author_gender":
                    setattr(meta, key, request.form[key])
                else:   
                    if request.form[key] != 'na':
                        meta.perceived_author_gender = request.form[key]

            meta.status = 'needs_crosscheck'
            meta.user_id = current_user.id 
            meta.last_edited = datetime.date.today().strftime("%Y-%m-%d")


            db.session.commit()
            return render_template("success.html", aps_id=aps_id) 
            #return request.form
    else:
        return(redirect(url_for('data.index')))


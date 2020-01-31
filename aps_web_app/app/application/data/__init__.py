from flask import Blueprint, render_template, request, redirect, url_for
from application.models import *
from flask_login import current_user
from  sqlalchemy.sql.expression import func

data_blueprint = Blueprint('data', __name__, template_folder='templates')

@data_blueprint.route("/")
@data_blueprint.route("/<aps_id>")
def index(aps_id=None):
    if not current_user.is_authenticated or not current_user.is_admin:
        return render_template("index.html", aps_id=None, endpoint=None)
    else:
        if aps_id:
            row = Review().query.filter(Review.record_id == aps_id).one_or_none()
            endpoint = row.url_doc_view

            return render_template("index.html", aps_id=aps_id, row=row, endpoint=endpoint)
        
        else:
        	#change to rand() for mysql
            row = Review().query.filter(Review.status == 'needs_audit').order_by(func.random()).first()
            try:
            	aps_id = row.record_id
            	endpoint = row.url_doc_view
            except: 
            	aps_id = ""
            	endpoint = ""
            return render_template("index.html", aps_id=aps_id, row=row, endpoint=endpoint)

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
            meta.status = 'done'
            db.session.commit()
            return render_template("success.html", aps_id=aps_id) 
            #return request.form
    else:
        return(redirect(url_for('data.index')))


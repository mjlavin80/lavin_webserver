from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_security import login_required
from flask_admin import Admin#, AdminIndexView, BaseView, expose
from application.models import *
from application.views import *
from flask_bcrypt import Bcrypt
from application.forms import *
from config import *
from datetime import datetime
import json

def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (getattr(form, field).label.text, error)
            errs.append(text)
    return errs

app = Flask(__name__)

app.secret_key = 'gskkrkemensbagakdoeksmss'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

#admin instance
admin = Admin(app, index_view=CustomBaseView(url='/admin'), name='Humanities Data', template_mode='bootstrap3', )

#required user loader method
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('admin.index'))

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/datastream")
def datastream():
    def setkeys(d):
        #build href using id
        d["more_link"] = "".join(["<a href='/resources/", str("".join([i for i in str(d["id"]) if i.isalpha() == False])), "'>Full Record</a>"])
        d["excerpt"] = "".join([" ".join(d["description"].split(" ")[:9]), " ..."])
        
        del d["id"]
        del d["_sa_instance_state"]
        return d
    #get from db
    rows = db.session.query(Resource).filter(Resource.status=='published').all()
    r = [setkeys(u.__dict__) for u in rows]
    #jsonify
    json_data = json.dumps(r)
    #return json_data
    return json_data

@app.route("/test_db")
@login_required
def test():
    try:
        password = 'goblin55'
        hashed = bcrypt.generate_password_hash(password)
        ins = User(username='mjlavin80', is_admin=True, display_name='Matt', email='digitalmedialab@pitt.edu', password=hashed, authenticated=True)

        try:
            db.session.add(ins)
            db.session.commit()
        except:
            db.session.rollback()
        return "success"
    except Exception, exc:
        db.session.rollback()
        error=exc.decode('utf8', errors='replace')
        return error

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/resources")
@app.route("/resources/<_id>")
def resources(_id=None):
    if _id:
        return "Endpoint for " + str(_id) + " in view mode"
    else:
        return render_template("search.html")

@app.route("/resources/<_id>/edit/<edit_id>", methods=["GET", "POST"])
@login_required
def edit_resources(_id=0, edit_id=0):
    if _id != 0:
        if edit_id != _id:
            return redirect(url_for("edit_resources", _id=_id, edit_id=_id))
        else:
            return "Endpoint for " + str(_id) + " in edit mode"
    else:
        return redirect(url_for("resources"))

@app.route("/approve", methods=["GET", "POST"])
@login_required
def approve():
    try:
        instruction = request.form.keys()[0].split("_")

        if "edit" in instruction:

            #get id
            return redirect(url_for("resource/edit"))
        if "approve" in instruction:
            #get id
            return (render_template("success.html"))
    except:
        pass

    #for testing
    q_ids = Resource.query.all()
    #q_ids = Resource.query.filter(Resource.status=="draft").all()

    approval_q = request.form.getlist('check-list[]')

    if request.method == 'POST' and len(approval_q) > 0:
        for _id in approval_q:
            to_update = Resource.query.filter(Resource.id==_id).one_or_none()
            to_update.status = "published"
            db.session.commit()
    return render_template("approve.html", approval_q= approval_q, q_ids=q_ids)

@app.route("/submit/<resource_type>", methods=["GET", "POST"])
@app.route("/submit", methods=["GET", "POST"])
def submit(resource_type=None):
    if resource_type != "dataset" and resource_type != "recipe" and resource_type != None:
        return redirect(url_for("submit"))
    add_resource = AddResource(request.form)

    if request.method == 'POST':
        if add_resource.validate():
            date = datetime.now()
            #add to db
            ins = Resource()
            ins.title = add_resource.title.data
            ins.description = add_resource.description.data
            ins.uri = add_resource.uri.data
            ins.submitted_by = add_resource.submitted_by.data
            ins.email = add_resource.email.data
            ins.date = date
            ins.resource_type = request.form['resource_type']

            if ins.resource_type == "dataset":
                ins.modified = add_resource.modified.data
                ins.publisher = add_resource.publisher.data
                ins.contact_point = add_resource.identifier.data
                ins.identifier = add_resource.identifier.data
                ins.access_level = add_resource.access_level.data
                ins.bureau_code = add_resource.bureau_code.data
                ins.license = add_resource.license.data
                ins.rights = add_resource.rights.data
                ins.spatial = add_resource.spatial.data
                ins.temporal = add_resource.temporal.data

            if current_user.is_admin:
                ins.status = "published"
            else:
                ins.status = "draft"
            # split on commas, make sure no single tag is too long
            suggested_tags = [x.strip() for x in add_resource.tags.data.split(',')]
            for a_tag in suggested_tags:
                if len(a_tag) > 30:
                    return render_template("errors.html", errors=['One or more tags exceeds max tag length (30 characters)'])
                else:
                    # append tags to tags
                    for i in suggested_tags:
                        #insert
                        newtag = Tag.query.filter(Tag.tagname==i).one_or_none()
                        if newtag is not None:
                            ins.tags.append(newtag)
                        else:
                            newtag = Tag(tagname=i)
                            db.session.add(newtag)
                            db.session.commit()
                            just_added = Tag.query.filter(Tag.tagname==i).one_or_none()
                            if newtag is not None:
                                ins.tags.append(just_added)
            try:
                db.session.add(ins)
                db.session.commit()
            except Exception, exc:
                db.session.rollback()
                error=exc.decode('utf8', errors='replace')
                return error

            return render_template("success.html", add_resource=add_resource)
        else:
            errors = compile_errors(add_resource)
            return render_template("errors.html", add_resource=add_resource, errors=errors)
    return render_template("submit.html", add_resource=add_resource, resource_type=resource_type)

@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    #for local dev
    app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    #app.run(host='0.0.0.0', debug=True, port=80)

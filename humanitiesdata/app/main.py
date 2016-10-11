from flask import Flask, render_template, request, redirect, url_for, flash, abort
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
from application.form_processors import *

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
    return redirect(url_for('login') )

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def index():
    return render_template("main.html")

@app.route("/datastream")
def datastream():
    #get from db
    rows = db.session.query(Resource).filter(Resource.status=='published').all()
    r = [setkeys(u.__dict__) for u in rows]
    #jsonify
    json_data = json.dumps(r)
    #return json_data
    return json_data

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tags")
@app.route("/tags/<tagname>")
def tags(tagname=None):
    if tagname:
        rows = Resource.query.join(Tag.resources).filter(Tag.tagname == tagname).all()
        if len(rows) == 0:
            return redirect(url_for('tags', tagname=None))
        r = [setkeys(u.__dict__) for u in rows]
        #jsonify
        json_data = json.dumps(r)
        return render_template("tags.html", tagname=tagname, json_data = json_data)
    else:
        all_tags = [i.tagname for i in Tag.query.all()]
        return render_template("tags.html", all_tags=all_tags)

@app.route("/resources")
@app.route("/resources/<_id>")
def resources(_id=None):
    if _id:
        obj = Resource.query.filter(Resource.id == _id).one_or_none()
        if not obj:
            return redirect(url_for('resources', _id=None))
        tags_ = [str(i.tagname) for i in obj.tags]
        return render_template("single_resource.html", tags=tags_, obj=obj.__dict__)
    else:
        return render_template("search.html")

@app.route("/resources/<_id>/edit", methods=["GET", "POST"])
@login_required
def edit_resources(_id=0):
    if _id != 0:
        #get resource_type
        r = Resource.query.filter(Resource.id==_id).one_or_none()
        return process_resource(request, "edit", _id=_id, resource_type=r.resource_type)
    else:
        return redirect(url_for("resources"))

@app.route("/approval", methods=["GET", "POST"])
@login_required
def approve():
    try:
        instruction = request.form.keys()[0].split("_")
        if instruction[0] == "approve":
            _id = instruction[1]
            to_update = Resource.query.filter(Resource.id==_id).one_or_none()
            to_update.status = "published"
            db.session.commit()
            return render_template("approve.html", approval_q=approval_q, q_ids=q_ids)
    except:
        pass
    #for testing
    #q_ids = Resource.query.all()
    q_ids = Resource.query.filter(Resource.status=="draft").all()

    approval_q = request.form.getlist('check-list[]')

    if request.method == 'POST' and len(approval_q) > 0:
        for _id in approval_q:
            to_update = Resource.query.filter(Resource.id==_id).one_or_none()
            to_update.status = "published"
            db.session.commit()
    return render_template("approve.html", approval_q=approval_q, q_ids=q_ids)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    signupform = SignupForm(request.form)
    if request.method == 'POST':
        if signupform.validate():
            new_signup = Signup()
            signupform.populate_obj(new_signup)
            new_signup.date = datetime.now()
            db.session.add(new_signup)
            db.session.commit()
            return render_template("signup.html", signupform=signupform, status="success")
        else:
            errors = compile_errors(signupform)
            return render_template("signup.html", signupform=signupform, status="error", errors=errors)
    else:
        return render_template("signup.html", signupform=signupform)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = form.data['username']
        user = User().query.filter(User.username==u).one()
        #check password
        next = request.args.get('next')
        if bcrypt.check_password_hash(user.password, form.data['password']):
            login_user(user)

            flash('Logged in successfully.')

            return redirect(next or url_for('login'))
        else:
            flash('Bad password.')
            return redirect(url_for('login'))
        if not next_is_valid(next):
            return abort(400)
    return render_template('login.html', form=form)

@app.route("/submit/<resource_type>", methods=["GET", "POST"])
@app.route("/submit", methods=["GET", "POST"])
def submit(resource_type=None):
    return process_resource(request, "submit", resource_type=resource_type)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        logout_user()
    except:
        pass
    return redirect(url_for('index'))

if __name__ == "__main__":
    #for local dev
    app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    #app.run(host='0.0.0.0', debug=True, port=80)

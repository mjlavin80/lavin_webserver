from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from flask.ext.security import login_required
from flask_admin import Admin#, AdminIndexView, BaseView, expose
from application.models import *
from application.views import *
from flask.ext.bcrypt import Bcrypt
from application.forms import *
from config import *
from datetime import datetime

def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error)
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

#admin
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

@app.route("/login")
def login():
    return "Login page"

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/search")
def search():
    return render_template("search.html")

@login_required
@app.route("/approve", methods=["GET", "POST"])
def approve():
    q_ids = Resource.query.filter(Resource.status=="draft").all()
    #print q_ids
    approval_q = request.form.getlist('check-list[]')
    print approval_q
    if request.method == 'POST' and len(approval_q) > 0:
        for _id in approval_q:
            to_update = Resource.query.filter(Resource.id==_id).one_or_none()
            to_update.status = "published"
            db.session.commit()
    return render_template("approve.html", approval_q= approval_q, q_ids=q_ids)

@app.route("/submit", methods=["GET", "POST"])
def submit():
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
            ins.resource_type = add_resource.resource_type.data
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
            except:
                db.session.rollback()
                raise

            return render_template("success.html", add_resource=add_resource)
        else:
            errors = compile_errors(add_resource)
            return render_template("errors.html", add_resource=add_resource, errors=errors)
    return render_template("submit.html", add_resource=add_resource)

@app.route("/signup")
def signup():
    return render_template("signup.html")


if __name__ == "__main__":
    #for local dev
    app.run(host='0.0.0.0', debug=True)

    #for production
    #app.run(host='0.0.0.0', port=80)

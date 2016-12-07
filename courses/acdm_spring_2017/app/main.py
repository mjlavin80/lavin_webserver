from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
import os
from application.models import *
from application import db
from application.forms import LoginForm
from flask_login import login_required
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
from flask.ext.bcrypt import Bcrypt
from flask.ext.admin.base import MenuLink

def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (getattr(form, field).label.text, error)
            errs.append(text)
    return errs

app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)

#ends session so there's no mysql timeout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('login')
        else:
            return self.render('admin/index.html')

# Create menu links classes with reloaded accessible
class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated

# Create customized model view classes
class ModelViewUser(ModelView):
    column_exclude_list = ('password')
    can_create = False
    def on_form_prefill(self, form, id):
        form.password.data = '[current password hidden]'
    def on_model_change(self, form, User, is_created=False):
        a = b.hashpw(form.password.data.encode('utf8'), b.gensalt())
        User.password = a
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

class ModelViewAdmin(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative views here
admin.add_view(ModelViewAdmin(User, db.session))
admin.add_view(ModelViewAdmin(Reading, db.session))
admin.add_view(ModelViewAdmin(Assignment, db.session))
admin.add_view(ModelViewAdmin(Day, db.session))
admin.add_view(ModelViewAdmin(Week, db.session))
admin.add_view(ModelViewAdmin(Basics, db.session))
admin.add_view(ModelViewAdmin(Policy, db.session))

#required user loader method
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#helper function for decorator to pass global info to templates
def generate_site_data():
    basics = Basics.query.first()
    return basics

#app context processor for sitewide data. Use as a decorator @include_site_data after @app.route to include a variable called basics in rendered template
def include_site_data(fn):
    @app.context_processor
    def additional_context():
        basics = generate_site_data()
        return {"basics":basics}
    return fn

#Begin route declarations
@app.route("/")
@include_site_data
def index():
     return render_template("index.html")

@app.route("/policies")
@include_site_data
def policies():
    policies = Policy.query.all()
    return render_template("policies.html", policies=policies)

@app.route("/calendar")
@include_site_data
def calendar():
    #get weeks from db
    weeks = Week.query.order_by(Week.week_number).all()
    return render_template("calendar.html", weeks=weeks)

@app.route("/assignments/<this_assignment>")
@app.route("/assignments")
@include_site_data
def assignments(this_assignment="all"):
    if this_assignment != "all":
        #get assignment from db
        try:
            a = Assignment.query.filter(Assignment.link_title == this_assignment).one_or_none()
            if a == []:
                return redirect(url_for("assignments", assignments=[], this_assignment="all"))
            return render_template("assignments.html", assignments=[], this_assignment=a)
        except:
            return redirect(url_for("assignments", assignments=[], this_assignment="all"))
    else:
        a = Assignment.query.all()
        return render_template("assignments.html", assignments=a, this_assignment="all")

@app.route("/readings")
@include_site_data
def readings():
    try:
        days = Day.query.all()
        readings = []
        for d in days:
            for r in d.readings:
                readings.append(r)
    except:
        readings = []
    return render_template("readings.html", readings=readings)

@app.route("/bibliography")
@include_site_data
def biblio():
    #get items from Zotero
    return render_template("bibliography.html")

@app.route('/protected/<path:filename>')
@include_site_data
#login_required
def protected(filename):
    path = os.path.join(app.instance_path, 'protected')
    return send_from_directory(path, filename)

@app.route('/coming_soon')
@include_site_data
def coming_soon():
    return render_template("soon.html")

def compile_errors(form):
    errs = []
    for field, errors in form.errors.items():
        for error in errors:
            text = u"Error in the %s field - %s" % (getattr(form, field).label.text, error)
            errs.append(text)
    return errs

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""

    form = LoginForm()
    next = request.args.get('next')
    if form.validate():
        user = User.query.filter(User.username==form.username.data).one_or_none()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, force=True)
                next = request.args.get('next')
                flash("You have successfully logged in")
                return redirect(next or url_for('index'))
    #print(form.errors)
    errors = compile_errors(form)
    return render_template("login.html", form=form, errors=errors)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    next = request.args.get('next')
    flash("You have successfully logged out")
    return redirect(url_for('login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    #for production
    app.run(host='0.0.0.0', port=port)

    #for dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash, g, session
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
from wtforms.fields import TextAreaField
from flask.ext.github import GitHub
from config import GITHUB_ADMIN

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
# setup github-flask
github = GitHub(app)

#ends session so there's no mysql timeout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        try:
            current_user.is_admin == True
            return self.render('admin/index.html')
        except:
            return redirect(url_for('status', message="unauthorized"))

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
    column_formatters = dict(course_description=lambda v, c, m, p: m.course_description[:25]+ " ...")
    form_overrides = dict(description=TextAreaField, course_description=TextAreaField)
    form_widget_args = dict(description=dict(rows=10), course_description=dict(rows=10))
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
admin.add_view(ModelViewAdmin(Activity, db.session))
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
    return AdminUser.query.get(user_id)

#helper function for decorator to pass global info to templates
def generate_site_data():
    basics = Basics.query.first()
    return basics

#app context processor for sitewide data. Use as a decorator @include_site_data after @app.route to include a variable called basics in rendered template
def include_site_data(fn):
    @app.context_processor
    def additional_context():
        #site_basics
        basics = generate_site_data()
        #user_authorization

        return {"basics":basics}
    return fn

#Begin route declarations
@app.route("/")
@include_site_data
def index():
    print(current_user)
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

@app.route("/planner")
@include_site_data
def planner():
    #move all this to application folder?
    import datetime

    t = datetime.date.today()
    t = datetime.datetime.strptime("Thursday, January 5, 2017", "%A, %B %d, %Y").date()

    weeks = Week.query.order_by(Week.week_number).all()
    last_due = []
    next_due = []
    days_before = []
    days_after = []
    for week in weeks:
        for day in week.days:
            try:
                dayname = datetime.datetime.strptime(day.name, "%A, %B %d, %Y").date()
            except:
                dayname = t
            if dayname >= t:
                days_after.append(day)
            if dayname < t:
                days_before.append(day)

    def find_assignment(day_list, mode='before'):
        assign = 0
        due_days = []
        for day in day_list:
            if mode == 'before' and assign == 0:
                if len(day.assignments) > 0:
                    due_days.append(day)
                    #if found, append and change assign var to a 1
                    assign += 1
            elif mode != 'before':
                if len(day.assignments) > 0:
                    due_days.append(day)
        if mode == 'before':
            due_days = due_days[-1:]
        return due_days

    last_due = find_assignment(days_before)
    next_due = find_assignment(days_after, mode='after')
    print(next_due)
    try:
        _next_three = days_after[0:3]
    except:
        _next_three = []
        fake = Day()
        fake.name = "No data to display"
        _next_three.append(fake)
    try:
        _last = days_before[-1]
    except:
        _last = Day()
        _last.name = "No data to display"
    try:
        last_due_date = last_due[0]
        days_passed = t - datetime.datetime.strptime(last_due_date.name, "%A, %B %d, %Y").date()
        days_ago = days_passed.days
    except:
        last_due_date = Day()
        last_due_date.name = "No data to display"
        fake_assignment = Assignment()
        fake_assignment.link_title = "all"
        fake_assignment.title = "No data to display"
        last_due_date.assignments.append(fake_assignment)
        days_ago = 0
    try:
        next_due_date = next_due[0]
        days_to = datetime.datetime.strptime(next_due_date.name, "%A, %B %d, %Y").date() - t
        days_to_next = days_to.days
    except:
        next_due_date = Day()
        next_due_date.name = "No data to display"
        fake_assignment = Assignment()
        fake_assignment.link_title = "all"
        fake_assignment.title = "No data to display"
        next_due_date.assignments.append(fake_assignment)
        days_to_next = 0

    today = t.strftime("%A, %B %d, %Y").replace(" 0", " ")
    return render_template("planner.html", last=_last, next_three=_next_three, next_due_date=next_due_date, last_due_date=last_due_date, days_ago=days_ago, days_to_next=days_to_next, today=today)

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

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.after_request
def after_request(response):
    db.session.remove()
    return response

@github.access_token_getter
def token_getter():
    user = g.user
    if user is not None:
        return user.github_access_token

@app.route('/github-callback')
@github.authorized_handler
def authorized(access_token):
    next_url = request.args.get('next') or url_for('index')
    if access_token is None:
        return redirect(next_url)
    user = User.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = User(access_token)
        db.session.add(user)
    user.github_access_token = access_token
    db.session.commit()

    session['user_id'] = user.id
    return redirect(url_for('status'))

@app.route('/login')
def login():
    try:
        c_u = github.get('user')
        return "Already logged in."
    except:
        return github.authorize()

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('status'))

@app.route('/status')
def status(message=""):
    """
    try:
        c_u = github.get('user')
        if str(c_u['login']) == str(GITHUB_ADMIN):
            user = AdminUser.query.filter(AdminUser.username=='admin').one_or_none()
            user.authenticated = True
            db.session.add(user)
            db.session.commit()
            login_user(user, force=True)
    except:
        pass
    if message=="":
        if g.user:
            message="in"
        else:
            message="out"
    """
    user = AdminUser.query.filter(AdminUser.username=='admin').one_or_none()
    user.authenticated = True
    db.session.add(user)
    db.session.commit()
    login_user(user, force=True)
    message="in"
    return render_template('status.html', message=message)

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
    port = int(os.environ.get("PORT", 80))
    #for production
    #app.run(host='0.0.0.0', port=port)

    #for dev
    app.run(host='0.0.0.0', debug=True, port=5000)

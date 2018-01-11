from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash, g, session
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
import os
from application.models import *
from application import db
from application.forms import *
from application.form_processors import *
from flask_login import login_required
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
from flask.ext.bcrypt import Bcrypt
from flask.ext.admin.base import MenuLink
from wtforms.fields import TextAreaField
from flask.ext.github import GitHub
from config import GITHUB_ADMIN, TIMELINE_URL
from sqlalchemy.sql import and_
import json

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
        AdminUser.password = a
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
    return render_template("index.html")

@app.route("/policies")
@include_site_data
def policies():
    policies = Policy.filter(public == "True").query.all()
    return render_template("policies.html", policies=policies)

@app.route("/calendar")
@include_site_data
def calendar():
    #get weeks from db
    weeks = Week.query.order_by(Week.week_number).all()
    return render_template("calendar.html", weeks=weeks)

@app.route("/timeline")
@app.route("/timeline/<row>")
@include_site_data
def timeline(row=None):
    if row:
        import pandas as pd
        count = 0
        df = pd.DataFrame.from_csv(TIMELINE_URL)
        for j in df.iterrows():
            count +=1
            if int(row) == count:
                i = []
                for m in [0,1,4,5]:
                    try:
                        j[1][m] = int(j[1][m])
                    except:
                        pass
                for k in j[1]:
                    value = str(k).replace("\n", " ").replace("\t", " ")
                    if value =="nan":
                        value = ""
                    i.append(value)
                if i[20] == "":
                    i[20] == "#"

        return render_template("timeline_row.html", essay=i[20])
    else:
        return render_template("timeline.html")

@app.route("/timelinedata")
@include_site_data
def timelinedata():
    import pandas as pd

    df = pd.DataFrame.from_csv(TIMELINE_URL)

    timeline = """
    {
        $$$$title$$$$: {
                $$$$text$$$$: {
                    $$$$headline$$$$: $$$$Making the Book$$$$,
                    $$$$text$$$$:     $$$$A Digital Timeline of Events Related to the History of the Book.$$$$
                },
                $$$$media$$$$: {
                    $$$$url$$$$: $$$$https://upload.wikimedia.org/wikipedia/commons/d/de/Albion_Press%2C_1830s_woodcut_by_George_Baxter.jpg$$$$,
                    $$$$thumb$$$$: $$$$https://upload.wikimedia.org/wikipedia/commons/d/de/Albion_Press%2C_1830s_woodcut_by_George_Baxter.jpg$$$$
                }
        },
        $$$$events$$$$: [
    """
    count = 1
    for j in df.iterrows():
        i = []
        for m in [0,1,4,5]:
            try:
                j[1][m] = int(j[1][m])
            except:
                pass
        for k in j[1]:
            value = str(k).replace("\n", " ").replace("\t", " ")
            if value =="nan":
                value = ""
            i.append(value)
        if i[20] == "":
            i[20] == "#"
        #i[20]
        combo = i[10] + " <a target=\$$$$blank\$$$$ href=\$$$$" + "timeline/" + str(count) +"\$$$$>View Full Essay</a>"
        timeline += "{\n $$$$start_date$$$$: { \n $$$$year$$$$: $$$$"+i[0]+"$$$$,\n $$$$month$$$$: $$$$"+i[1]+"$$$$ },"

        if i[4] != "":
            timeline += "\n$$$$end_date$$$$: { \n $$$$year$$$$: $$$$"+i[4]
        else:
            timeline += "\n$$$$end_date$$$$: { \n $$$$year$$$$: $$$$"+i[0]
        if i[5] != "":
            timeline += "$$$$,\n $$$$month$$$$: $$$$"+i[5]+"$$$$ },"
        else:
            timeline += "$$$$,\n $$$$month$$$$: $$$$"+i[1]+"$$$$ },"

        timeline += "\n$$$$display_date$$$$: $$$$"+ i[8]+"$$$$,"
        timeline += "\n$$$$media$$$$: { \n $$$$url$$$$: $$$$"+ i[11]+"$$$$ ,\n $$$$credit$$$$: $$$$"+ i[12]+"$$$$ ,\n $$$$caption$$$$: $$$$"+i[13]+"$$$$,\n $$$$thumb$$$$: $$$$"+i[14]+"$$$$ },"
        timeline += "\n$$$$text$$$$: { \n $$$$headline$$$$: $$$$"+ i[9]+"$$$$ ,\n $$$$text$$$$: $$$$" + combo +"$$$$ },"
        timeline += "\n$$$$type$$$$: $$$$overview$$$$ \n },"
        count +=1
    timeline = timeline[:-1]
    timeline += """
    ]
    }
    """
    timeline = timeline.replace("\"", "&#34;")
    timeline = timeline.replace("\'", "&#39;")
    timeline = timeline.replace("$$$$", "\"")

    return timeline

@app.route("/planner")
@include_site_data
def planner():
    try:
        c_u = github.get('user')

        if str(c_u['login']) == str(GITHUB_ADMIN):
            #move all this to application folder?
            import datetime
            t = datetime.date.today()

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
        else:
            return redirect(url_for("login"))
    except:
        return redirect(url_for("login"))
@app.route("/assignments/<this_assignment>")
@app.route("/assignments")
@include_site_data
def assignments(this_assignment="all"):
    if this_assignment != "all":
        #get assignment from db
        try:
            a = Assignment.query.filter(Assignment.link_title == this_assignment and public == "True").one_or_none()
            if a == []:
                return redirect(url_for("assignments", assignments=[], this_assignment="all"))
            return render_template("assignments.html", assignments=[], this_assignment=a)
        except:
            return redirect(url_for("assignments", assignments=[], this_assignment="all"))
    else:
        a = Assignment.query.all()
        return render_template("assignments.html", assignments=a, this_assignment="all")

@app.route("/activities/<this_activity>")
@app.route("/activities")
@include_site_data
def activities(this_activity="all"):
    if this_activity != "all":
        #get activity from db
        a = Activity.query.filter(Activity.id == this_activity).one_or_none()
        if a:
            return render_template("activities.html", activities=[], this_activity=a)
        else:
            a = Activity.query.filter(public == "True").all()
            a.sort(key=lambda x: x.day.id)
            return render_template("activities.html", activities=a, this_activity="all")
    else:
        a = Activity.query.filter(public == "True").all()
        a.sort(key=lambda x: x.day.id)
        return render_template("activities.html", activities=a, this_activity="all")

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

@app.route("/processor", methods=["GET", "POST"])
@app.route("/processor/<resource_type>", methods=["GET", "POST"])
@include_site_data
def processor(resource_type=None):
    valid = False
    if resource_type:
        if resource_type=="activity":
            createform = CreateActivity(request.form)
            if createform.validate():
                new = Activity()
                valid=True
        if resource_type=="reading":
            createform = CreateReading(request.form)
            if createform.validate():
                new = Reading()
                valid=True
        if resource_type=="assignment":
            createform = CreateAssignment(request.form)
            if createform.validate():
                new = Assignment()
                valid=True
        if resource_type=="collection":
            createform = CreateCollection(request.form)
            collection_items = request.form["coll_data"]
            if createform.validate():
                new = Collection()
                valid=True


        if valid==True:
            createform.populate_obj(new)
            #get current_user id
            #make into a function
            try:
                u_id = get_current_user_id()
            except:
                #add user data to Activity
                u_id = 11
                new.user_id = u_id

            db.session.add(new)
            db.session.commit()
            #ad hoc rules for collection
            if resource_type=="collection":
                #process extra form data
                collection_items = json.loads(collection_items)
                for h, i in enumerate(collection_items):

                    _type, _id = i.split('-')
                    type_dict = {"activity": Activity(), "assignment": Assignment(), "reading": Reading()}
                    #get the object
                    if new.public=="True":
                        child_content = type_dict[_type].query.filter_by(id=_id).first()
                        child_content.public = "True"
                        db.session.add(child_content)
                        db.session.commit()
                    new_coll_item = CollectionItems()
                    new_coll_item.collection_id = new.id
                    new_coll_item.target_table = _type
                    new_coll_item.target_id = _id
                    new_coll_item.order = h
                    db.session.add(new_coll_item)
                    db.session.commit()
            return render_template("processor.html", status="success")
        else:
            errors = compile_errors(createform)
            return render_template("processor.html", status="error", errors=errors)

@app.route("/create", methods=["GET", "POST"])
@app.route("/create/<resource_type>", methods=["GET", "POST"])
@include_site_data
def create(resource_type=None):
    #handle form selection
    rtype=None
    if request.method == "POST":
        rtype=request.form["type"]
    if rtype:
        return redirect(url_for('create', resource_type=rtype))
    if resource_type:
        if resource_type=="activity":
            createactivityform = CreateActivity(request.form)
            return render_template("create_activity.html", resource_type=resource_type, createactivityform=createactivityform)
        if resource_type=="reading":
            createreadingform = CreateReading(request.form)
            return render_template("create_reading.html", resource_type=resource_type, createreadingform=createreadingform)
        if resource_type=="assignment":
            createassignmentform = CreateAssignment(request.form)
            return render_template("create_assignment.html", resource_type=resource_type, createassignmentform=createassignmentform)
        if resource_type=="collection":
            createcollectionform = CreateCollection(request.form)
            try:
                u_id = get_current_user_id()
            except:
                #add user data to Activity
                u_id = 11
            # my readings
            readings = Reading.query.filter(Reading.user_id==u_id).all()
            # my assignments
            assignments = Assignment.query.filter(Assignment.user_id==u_id).all()
            # my activities
            activities = Activity.query.filter(Activity.user_id==u_id).all()
            # public content
            p_r = Reading.query.filter(and_(Reading.public=="True", Reading.user_id != u_id)).all()
            p_as = Assignment.query.filter(and_(Assignment.public=="True", Assignment.user_id != u_id)).all()
            p_act = Activity.query.filter(and_(Activity.public=="True", Activity.user_id != u_id)).all()
            public = {"readings":p_r, "assignments":p_as, "activities":p_act}
            all_content = {"readings":readings, "assignments":assignments, "activities": activities, "public": public}

            return render_template("create_collection.html", resource_type=resource_type, all_content=all_content, createcollectionform=createcollectionform)
    else:
        return render_template("create.html", resource_type=resource_type)

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
        g.user = GithubToken.query.get(session['user_id'])

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
    user = GithubToken.query.filter_by(github_access_token=access_token).first()
    if user is None:
        user = GithubToken(access_token)
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
    try:
        logout_user()
    except:
        pass
    return redirect(url_for('index'))

@app.route('/status')
def status(message=""):
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
    #for debugging locally
    """
    user = AdminUser.query.filter(AdminUser.username=='admin').one_or_none()
    user.authenticated = True
    db.session.add(user)
    db.session.commit()
    login_user(user, force=True)
    message="in"
    """
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

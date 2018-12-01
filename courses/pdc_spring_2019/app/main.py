import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash, g, session
from flask_admin import Admin
from application.models import *
from application.user_controls import *
from application import db
from application.forms import *
from application.form_processors import *
from flask_login import login_required
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_github import GitHub
from config import GITHUB_ADMIN, ASANA_CODE, ASANA_PROJECT_ID
from sqlalchemy.sql import and_, or_
import json, requests
import datetime
import pandas as pd

app = Flask(__name__)
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
# setup github-flask
github = GitHub(app)

#ends session so there's no mysql timeout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative and user views here
admin.add_view(ModelViewAdmin(UserProfile, db.session))
admin.add_view(ReadingViewAdmin(Reading, db.session))
admin.add_view(ModelViewAdmin(Assignment, db.session))
admin.add_view(ModelViewAdmin(Activity, db.session))
admin.add_view(ModelViewAdmin(Day, db.session))
admin.add_view(ModelViewAdmin(Week, db.session))
admin.add_view(ModelViewAdmin(Basics, db.session))
admin.add_view(ModelViewAdmin(Policy, db.session))
admin.add_view(ModelViewUser(Dataset, db.session))
admin.add_view(ModelViewUser(TimelineEntry, db.session))
admin.add_view(ModelViewBlog(BlogPost, db.session))
admin.add_view(ModelViewTag(Tag, db.session))

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
    return UserProfile.query.get(user_id)

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
    policies = Policy.query.filter(Policy.public == "True").all()
    return render_template("policies.html", policies=policies)

@app.route("/required_book")
@include_site_data
def required_book():
    book_policy = Policy.query.filter(and_(Policy.public == "True", Policy.title =="Required Texts")).all()
    return render_template("required_book.html", book_policy=book_policy)

@app.route("/calendar")
@include_site_data
def calendar():
    #get weeks from db
    weeks = Week.query.order_by(Week.week_number).all()
    return render_template("calendar.html", weeks=weeks)

@app.route("/timeline")
@app.route("/timeline/<entry_id>")
@include_site_data
def timeline(entry_id=None):
    if entry_id:
        timeline_entry= TimelineEntry.query.filter(TimelineEntry.id == entry_id).one_or_none()
        return render_template("timeline_row.html", timeline_entry=timeline_entry)
    else:
        return render_template("timeline.html")

@app.route("/timelinedata")
@include_site_data
def timelinedata():

    timeline_rows = TimelineEntry.query.all()
    return render_template("timelinedata.json", timeline_rows=timeline_rows)

@app.route("/blogs")
@app.route("/blogs/")
@app.route("/blogs/<blog_id>")
@app.route("/blogs/<blog_id>/posts")
@app.route("/blogs/<blog_id>/posts/")
@app.route("/blogs/<blog_id>/posts/<post_id>")
@include_site_data
def blogs(blog_id=None, post_id=None):
    # assume custom title, try to translate to user_id, if it fails treat blog id as a user id
    if blog_id:
        users = UserProfile.query.all()
        custom_titles = []
        #edit this to look for a path, not a title
        for i in users:
            try: 
                url = quote(i.custom_blog_title.lower().replace(" ", "-"))
                custom_titles.append((i.id, url))
            except:
                pass
        custom_id = [i[0] for i in custom_titles if i[1] == blog_id]
        if len(custom_id) > 0:
            if post_id:
                # look up by path or id

                result = "custom blog, one post"
            else:
                all_posts = BlogPost.query.filter(BlogPost.user_id == custom_id[0]).all()
                result = "custom blog, no post"
        else:
            if post_id:
                # look up by path or id
                result= "blog id, one post"
            else:
                all_posts = BlogPost.query.filter(BlogPost.user_id == blog_id).all()
                result= "blog id, no post"

        return result
    else:
        return "no blog selected"

@app.route("/planner")
@include_site_data
def planner():
    try:
        current_user.is_admin == True
    

        ASANA_BASE_URL = 'https://app.asana.com/api/1.0/'
        
        h = {"Authorization": "Bearer "+ ASANA_CODE}
        r = requests.get(ASANA_BASE_URL + "projects/" + ASANA_PROJECT_ID + "/tasks", headers=h) 
        all_tasks = json.loads(r.text)['data']
        project_tasks = []

        for t in all_tasks:
            r2 = requests.get(ASANA_BASE_URL + "tasks/" + str(t['id']), headers=h)
            full_task = json.loads(r2.text)['data']
            if not full_task['completed']:
                project_tasks.append(full_task)

        def sort_key(d):
            if d['due_on']:
                return d['due_on']
            else:
                return '9999-99-99'

        project_tasks = sorted(project_tasks, key=sort_key, reverse=False)
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
        return render_template("planner.html", project_tasks=project_tasks, last=_last, next_three=_next_three, next_due_date=next_due_date, last_due_date=last_due_date, days_ago=days_ago, days_to_next=days_to_next, today=today)

    except:
        return redirect(url_for('status', message="unauthorized"))

@app.route("/assignments/<this_assignment>")
@app.route("/assignments")
@include_site_data
def assignments(this_assignment="all"):
    if this_assignment != "all":
        #get assignment from db
        try:
            a = Assignment.query.filter(and_(Assignment.link_title == this_assignment, Assignment.public == "True")).one_or_none()
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
            a = Activity.query.filter(Activity.public == "True").all()
            a.sort(key=lambda x: x.day.id)
            return render_template("activities.html", activities=a, this_activity="all")
    else:
        a = Activity.query.filter(Activity.public == "True").all()
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
    #need to check if github username is in user_profile
    user = False
    try:
        c_u = github.get('user')
        user = UserProfile.query.filter(UserProfile.username==c_u['login']).one_or_none()
    except:
        message="out"

        #for debugging locally
    
        user = UserProfile.query.filter(UserProfile.id==1).one_or_none()
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        login_user(user, force=True)
        message="in"

        # end local debugging block

        return render_template('status.html', message=message)
    if user: 
        user.authenticated = True
        user.is_admin = True
        db.session.add(user)
        db.session.commit()
        login_user(user, force=True)
        message="in"
    else:
        message="unauthorized"
      
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

db.init_app(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    #for production
    #app.run(host='0.0.0.0', port=port)
    #for dev
    app.run(host='0.0.0.0', debug=True, port=5000)

import os
from flask import abort, Flask, render_template, make_response, redirect, url_for, send_from_directory, request, flash, g, session
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
from urllib.parse import quote
from application.planner import planner_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(planner_blueprint)

bcrypt = Bcrypt(app)
# setup github-flask
github = GitHub(app)

#ends session so there's no mysql timeout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative and user views here

admin.add_view(ReadingViewAdmin(Reading, db.session))
admin.add_view(ModelViewAdmin(Assignment, db.session))
admin.add_view(ModelViewAdmin(Activity, db.session))
admin.add_view(ModelViewAdmin(Day, db.session))
admin.add_view(ModelViewAdmin(Week, db.session))
admin.add_view(ModelViewAdmin(Basics, db.session))
admin.add_view(ModelViewAdmin(Policy, db.session))
admin.add_view(ModelViewUserProfile(UserProfile, db.session))
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

@app.route("/feeds/<blog_id>")
@include_site_data
def feeds(blog_id=None):
    if blog_id:
        source_user = UserProfile.query.filter(or_(UserProfile.id == blog_id, UserProfile.custom_blog_path==quote(blog_id))).one_or_none()
        if not source_user:
            abort(404)
        all_posts = BlogPost.query.filter(BlogPost.user_id == source_user.id).all()
        if not all_posts:
            all_posts = []
        template = render_template('rss.xml', all_posts=all_posts, source_user=source_user)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response
            
    else:
        redirect(url_for('blogs'))


@app.route("/tags")
@app.route("/tags/")
@app.route("/tags/<tag_path>")
@include_site_data
def tags(tag_path=None):
    # assume custom title, try to translate to user_id, if it fails treat blog id as a user id
    if tag_path:
        source_tag = Tag.query.filter(Tag.tag_path == tag_path).one_or_none()

        if not source_tag:
            abort(404)
        #get all posts with the tag
        all_posts = BlogPost.query.all()
        if all_posts: 
            with_tag = [p for p in all_posts if source_tag in p.tags]
            if with_tag:
                blog_paths = []
                for post in with_tag:
                    source_user = UserProfile.query.filter(UserProfile.id == post.user_id).one_or_none()
                    blog_path = source_user.custom_blog_path
                    blog_paths.append(blog_path)
                # return template
                return render_template("tag_main.html", with_tag=with_tag, source_tag=source_tag, blog_paths=blog_paths)
            else:
                #return template
                return render_template("tag_main.html", with_tag=[], source_tag=source_tag, blog_paths=[])
        else:
            #return template
            return render_template("tag_main.html", with_tag=[], source_tag=source_tag, blog_paths=[])      
    else:    
        #get all tags 
        all_tags = Tag.query.all()
        all_posts = BlogPost.query.all()
        #count blog posts for each user/blog and get 
        post_counts = []
        for tag in all_tags:
            post_count = len([i for i in all_posts if tag in i.tags])
            post_counts.append(post_count)
        
        #return template
        return render_template("all_tags.html", all_tags=all_tags, post_counts=post_counts)

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
        source_user = UserProfile.query.filter(or_(UserProfile.id == blog_id, UserProfile.custom_blog_path==quote(blog_id))).one_or_none()
        
        if not source_user:
            abort(404)
        if post_id:
            # look up by path or id
            this_post = BlogPost.query.filter(or_(BlogPost.id == post_id, BlogPost.post_path == quote(post_id))).one_or_none()
            if not this_post:
                abort(404)
            return render_template("blog_post.html", this_post=this_post, source_user=source_user)
            
        else:
            all_posts = BlogPost.query.filter(BlogPost.user_id == source_user.id).all()
            if not all_posts:
                # return template
                return render_template("blog_main.html", all_posts=[], source_user=source_user)
            else:
                #return template
                return render_template("blog_main.html", all_posts=all_posts, source_user=source_user) 
    else:
        #get titles and urls of all user blogs 
        bloggers = UserProfile.query.all()
        
        #count blog posts for each user/blog
        blog_counts = []
        for blogger in bloggers:
            post_count = len(BlogPost.query.filter(BlogPost.user_id == blogger.id).all())
            blog_counts.append(post_count)
        #return template
        return render_template("all_blogs.html", bloggers=bloggers, blog_counts=blog_counts)

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
        return redirect(url_for('status'))
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
    user = False
    try:
        c_u = github.get('user')
        user = UserProfile.query.filter(UserProfile.username==c_u['login']).one_or_none()
        
        if user: 
            #check for approval 
            if user.approved:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, force=True)
                message="in"
            # else not approved 
            else: 
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, force=True)
                message="unapproved"
        else:
            # code for logged in but not registered
            message="unregistered"
    except:
        message="out"

        #for debugging locally
    
        # user = UserProfile.query.filter(UserProfile.id==1).one_or_none()
        # db.session.add(user)
        # db.session.commit()
        # login_user(user, force=True)
        # message="in"

        # end local debugging block

        return render_template('status.html', message=message)
      
    return render_template('status.html', message=message)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        try: 
            c_u = github.get('user')
            user = UserProfile()
            user.username = c_u['login']
            user.is_admin = 0
            user.display_name = request.form['display_name']
            user.email = request.form['email']
            user.authenticated = 1
            user.custom_blog_title = request.form['custom_blog_title']
            if request.form['custom_blog_title'] != "":
                user.custom_blog_path = quote(request.form['custom_blog_title'].lower().replace(" ", "-"))
            else:
                user.custom_blog_path = c_u['login']
            user.approved = 0
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('status')) 
        except:
            return redirect(url_for('status'))  
    else: 
        return redirect(url_for('status'))

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

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
    app.run(host='0.0.0.0', port=port)
    #for dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

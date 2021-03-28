import os
from config import *
from flask import abort, Flask, render_template, make_response, redirect, url_for, send_from_directory, request, flash, g, session
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_security import login_required
from flask_admin import Admin
from application import db
from application.models import *
from application.user_controls import *
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_github import GitHub
from flask_login import login_required
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_migrate import Migrate
import json, requests
from sqlalchemy.sql import and_, or_
from urllib.parse import quote
#from application.browse import browse_blueprint
#from application.tag import tag_blueprint


app = Flask(__name__)
app.config.from_pyfile('config.py')
#app.register_blueprint(browse_blueprint)

#bcrypt instance for password hashing
bcrypt = Bcrypt(app)

# setup github-flask
github = GitHub(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

#admin instance
admin = Admin(app, index_view=MyAdminIndexView(url='/admin'), name='Humanities Data', template_mode='bootstrap3', )

# Add administrative and user views here
admin.add_view(ModelViewUserProfile(UserProfile, db.session))
admin.add_view(ModelViewResource(Resource, db.session))
admin.add_view(ModelViewTag(Tag, db.session))
admin.add_view(ModelViewCollection(Collection, db.session))

#required user loader method
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = "login"

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login') )

@login_manager.user_loader
def load_user(user_id):
    return UserProfile.query.get(user_id)

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

# Begin route declarations
@app.route("/")
def index():
    return render_template("main.html")

@app.route("/datastream")
def datastream():
    #get from db
    rows = db.session.query(Resource).filter(Resource.public=='True').all()
    
    all_tags = []
    for u in rows:
        tags = [] 
        for i in u.tags:
            data = {"id":i.id, "tag_name":i.tag_name, "tag_path":i.tag_path}
            tags.append(data)    
        all_tags.append(tags)

    r = [setkeys(u.__dict__) for u in rows]
    
    r_w_tags = []
    for e, i in enumerate(r):
        i["tags"] = all_tags[e]
        r_w_tags.append(i)

    #jsonify
    json_data = json.dumps(r_w_tags)


    r = make_response(json_data)
    r.headers.set('Content-Type', 'application/json')
    r.headers.set('Accept', 'application/json')
    
    return r
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/tags")
@app.route("/tags/<tag_name>")
def tags(tag_name=None):
    if tag_name:
        rows = Resource.query.join(Tag.resources).filter(Tag.tag_name == tag_name).filter(Resource.public=='True').all()
        if len(rows) == 0:
            return redirect(url_for('tags', tag_name=None))
        #adds fields to resource
        r = [setkeys(u.__dict__) for u in rows]
        #jsonify
        json_data = json.dumps(r)
        return render_template("tags.html", tag_name=tag_name, json_data = json_data)
    else:
        _all = [i for i in Tag.query.all()]
    
    
    all_tags = []
    for tag in _all:
        published = [i for i in tag.resources if i.public == "True"]
        if len(published) > 0:
            all_tags.append(tag.tag_name)
    
    all_tags.sort()

    return render_template("tags.html", all_tags=all_tags)

@app.route("/resources")
@app.route("/resources/<_id>")
def resources(_id=None):
    if _id:
        obj = Resource.query.filter(Resource.id == _id).one_or_none()
        if not obj:
            return redirect(url_for('resources', _id=None))
        tags_ = [str(i.tag_name) for i in obj.tags]

        return render_template("single_resource.html", tags=tags_, obj=obj.__dict__, _id=_id)
    else:
        return render_template("search.html")


db.init_app(app)

if __name__ == "__main__":
    #for local dev
    # app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    app.run(host='0.0.0.0', debug=True, port=80)

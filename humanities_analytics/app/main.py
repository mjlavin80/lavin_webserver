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
from application.notebook.notebook import notebook_blueprint
from application.courses.courses import courses_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(notebook_blueprint)
app.register_blueprint(courses_blueprint)

#bcrypt instance for password hashing
bcrypt = Bcrypt(app)

# setup github-flask
github = GitHub(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

#admin instance
admin = Admin(app, index_view=MyAdminIndexView(url='/admin'), name='Humanities Analytics', template_mode='bootstrap3', )

# Add administrative and user views here
admin.add_view(ModelViewUserProfile(UserProfile, db.session))
admin.add_view(ModelViewNotebook(NotebookPost, db.session))
admin.add_view(ModelViewNotebookTag(NotebookTag, db.session))
admin.add_view(ModelViewAdmin(Syllabus, db.session))
admin.add_view(ModelViewAdmin(StaticPage, db.session))

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
    data = StaticPage.query.filter(StaticPage.route == "index").one_or_none()
    return render_template("main.html", data=data)

db.init_app(app)

if __name__ == "__main__":
    #for local dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    app.run(host='0.0.0.0', debug=True, port=80)

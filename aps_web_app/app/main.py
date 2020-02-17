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
from config import GITHUB_ADMIN
from sqlalchemy.sql import and_, or_
import json, requests
import datetime
from urllib.parse import quote
from application.data import data_blueprint

app = Flask(__name__)
app.config.from_pyfile('config.py')

#blueprints
app.register_blueprint(data_blueprint)

#bcrypt instance for password hashing
bcrypt = Bcrypt(app)

# setup github-flask
github = GitHub(app)

#ends session so there's no mysql timeout
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative and user views here
admin.add_view(ModelViewUserProfile(UserProfile, db.session))
admin.add_view(ModelViewStatic(StaticPage, db.session))
admin.add_view(ModelViewReview(Review, db.session))
admin.add_view(ModelViewAdmin(Publication, db.session))
admin.add_view(ModelViewAdmin(Contributor, db.session))
admin.add_view(ModelViewReview(ExtractedParsed, db.session))

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

# Begin route declarations

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
    next_url = request.args.get('next') or url_for('data.index')
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
    return redirect(url_for('data.index'))
    

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
    
        #user = UserProfile.query.filter(UserProfile.id==1).one_or_none()
        #db.session.add(user)
        #db.session.commit()
        #login_user(user, force=True)
        #message="in"

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
def page_not_allowed(e):
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

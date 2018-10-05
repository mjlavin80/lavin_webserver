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
from flask_bcrypt import Bcrypt
from flask_admin.base import MenuLink
from wtforms.fields import TextAreaField
from flask_github import GitHub
from config import GITHUB_ADMIN
from sqlalchemy.sql import and_
from  sqlalchemy.sql.expression import func
from flask_admin.form import rules
import json
from flask import Markup
import requests
from bs4 import BeautifulSoup

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
    column_formatters = dict(corrected_transcription=lambda v, c, m, p: m.corrected_transcription[:25]+ " ...", ocr_transcription=lambda v, c, m, p: m.ocr_transcription[:25]+ " ...")
    #form_overrides = dict(corrected_transcription=TextAreaField, ocr_transcription=TextAreaField)
    #form_widget_args = dict(corrected_transcription=dict(rows=10), ocr_transcription=dict(rows=10))

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return current_user.is_authenticated
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login'))

class MetaViewAdmin(ModelViewAdmin):
    def _url_formatter(view, context, model, name):
        return Markup(
            u"<a href='%s' target='blank'>NYT Link</a>" % model.nyt_pdf_endpoint if model.nyt_pdf_endpoint else u"")
    column_formatters = dict(corrected_transcription=lambda v, c, m, p: m.corrected_transcription[:25]+ " ...", ocr_transcription=lambda v, c, m, p: m.ocr_transcription[:25]+ " ...")
    column_formatters['nyt_pdf_endpoint'] = _url_formatter
    column_filters = ('review_type',)
    #column_list = ['nyt_id', 'review_type', 'headline', 'byline', 'pub_date', 'ocr_transcription', 'corrected_transcription', 'metadata_work']
    column_exclude_list = ('month', 'year', 'byline', 'corrected_transcription','document_type', 'page', 'word_count')
    form_excluded_columns = ('month', 'year', 'byline', 'corrected_transcription','document_type', 'page')

admin = Admin(app, name='Dashboard', template_mode='bootstrap3', index_view=MyAdminIndexView())

# Add administrative views here
admin.add_view(ModelViewAdmin(User, db.session))
admin.add_view(MetaViewAdmin(Metadata, db.session))
admin.add_view(ModelViewAdmin(Work, db.session))
admin.add_view(ModelViewAdmin(Author, db.session))

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

#Begin route declarations
@app.route("/")
@app.route("/<nyt_id>")
def index(nyt_id=None):
    if current_user.is_authenticated and current_user.is_admin:
        if nyt_id != None:
            row = Metadata().query.filter(Metadata.nyt_id == nyt_id).one_or_none()
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')

            return render_template("index.html", nyt_id=nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link)
        else:
            row = Metadata().query.filter(and_(Metadata.year > 1905, Metadata.year < 1923)).filter(Metadata.review_type.like("needs_audit%")).filter(Metadata.page == 'BR2').order_by(func.rand()).first()
            # BR1, 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'BR8', 'BR9', 'BR10'
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')

            return render_template("index.html", nyt_id=row.nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link) 
    else:
        return render_template("index.html", nyt_id=None, endpoint=None)

@app.route("/f")
@app.route("/f/<nyt_id>")
def female(nyt_id=None):
    if current_user.is_authenticated and current_user.is_admin:
        if nyt_id != None:
            row = Metadata().query.filter(Metadata.nyt_id == nyt_id).one_or_none()
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')

            return render_template("index.html", nyt_id=nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link)
        else:
            row = Metadata().query.filter(and_(Metadata.review_type == "needs_audit_probably_female", Metadata.year > 1905, Metadata.year < 1925)).order_by(func.rand()).first()
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')

            return render_template("index.html", nyt_id=row.nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link) 
    else:
        return render_template("index.html", nyt_id=None, endpoint=None, pdf_link=None)

@app.route("/m")
@app.route("/m/<nyt_id>")
def male(nyt_id=None):
    if current_user.is_authenticated and current_user.is_admin:
        if nyt_id != None:
            row = Metadata().query.filter(Metadata.nyt_id == nyt_id).one_or_none()
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')

            return render_template("index.html", nyt_id=nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link)
        else:
            row = Metadata().query.filter(and_(Metadata.review_type == "needs_audit_probably_male", Metadata.year > 1905, Metadata.year < 1925)).filter(Metadata.headline.like("%$%")).order_by(func.rand()).first()
            endpoint = row.nyt_pdf_endpoint
            r = requests.get(endpoint)
            html = BeautifulSoup(r.text, features="html.parser")
            link = html.find("a", {"class":"user-action archive-user-action"})
            pdf_link = link['href'].replace('.html', '.pdf')
            
            return render_template("index.html", nyt_id=row.nyt_id, row=row, endpoint=endpoint, pdf_link=pdf_link) 
    else:
        return render_template("index.html", nyt_id=None, endpoint=None, pdf_link=None)

@app.route("/update_meta", methods=["GET", "POST"])
@app.route("/update_meta/<nyt_id>", methods=["GET", "POST"])
def update_meta(nyt_id=None):
    if request.method == 'POST':
        meta = Metadata().query.filter(Metadata.nyt_id == nyt_id).one_or_none()
        meta.review_type = request.form['review_type_data']
        if request.form['gender_label_data'] != 'na':
            meta.perceived_author_gender = request.form['gender_label_data']
        db.session.commit()
        return render_template("success.html", nyt_id=nyt_id) 
    else:
        return(redirect(url_for('index')))

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

    # user = AdminUser.query.filter(AdminUser.username=='admin').one_or_none()
    # user.authenticated = True
    # db.session.add(user)
    # db.session.commit()
    # login_user(user, force=True)
    # message="in"

    #end local debug block

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
    app.run(host='0.0.0.0', port=port)
    #for dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

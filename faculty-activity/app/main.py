from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_security import login_required
from flask_admin import Admin#, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from application.models import *
from application.views import *
from flask_bcrypt import Bcrypt
from application.forms import *
from config import *
from datetime import datetime
import json


app = Flask(__name__)

app.secret_key = 'gskkrkemensbagakdoeksmss'
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


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

#admin instance
admin = Admin(app, index_view=CustomBaseView(url='/admin'), name='Faculty Activity Portfolio', template_mode='bootstrap3', )

# Add administrative views here
admin.add_view(ModelViewAdmin(Portfolio, db.session))

#required user loader method
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return redirect(url_for('login') )

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/cv", methods=["GET", "POST"])
def cv():
    data = Portfolio.query.filter(Portfolio.date == "cv").order_by(Portfolio.sort_order).all()
    return render_template("cv.html", data=data)

@app.route("/activity/<year>", methods=["GET", "POST"])
def activity(year):
    form = LoginForm()
    #get data and pass along
    data = Portfolio.query.filter(Portfolio.date == year).order_by(Portfolio.sort_order).all()
    return render_template("portfolio.html", data=data, year=year, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = form.data['username']
        user = User().query.filter(User.username==u).one_or_none()
        if user:
            #check password
            next = request.args.get('next')

            if bcrypt.check_password_hash(user.password, form.data['password']):
                login_user(user)
                flash('Logged in successfully.')
                return redirect(request.referrer or url_for('index'))
            else:
                flash('Bad user name or password.')
                return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        logout_user()
    except:
        pass
    return redirect(url_for('index'))

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
    #for local dev
    #app.run(host='0.0.0.0', debug=True, port=5000)

    #for production
    app.run(host='0.0.0.0', debug=True, port=80)

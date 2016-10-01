from flask_admin import AdminIndexView, BaseView, expose
from application.forms import *
from application.models import *
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, login_user, logout_user, current_user
from application import app, db
from flask_admin.contrib.sqla import ModelView

#custom access levels for admin
class ModelViewAdmin(ModelView):
    column_exclude_list = ('password')
    #can_create = False
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
        return redirect(url_for('admin.index'))

#admin view custom class
class CustomBaseView(AdminIndexView):
    @expose('/', methods=["GET", "POST"])
    def admin_index(self):
        bcrypt = Bcrypt(app)
        """For GET requests, display the login form. For POSTS, login the current user
        by processing the form."""

        form = LoginForm()
        next = request.args.get('next')
        if form.validate():
            user = User.query.filter(User.username==form.username.data).first()

            if user:
                a = bcrypt.generate_password_hash(form.password.data)
                if bcrypt.check_password_hash(user.password, form.password.data):
                    user.authenticated = True
                    db.session.add(user)
                    db.session.commit()
                    login_user(user, remember=True, force=True)
                    next = request.args.get('next')
                    print("You have successfully logged in")
                    return redirect(next or url_for('admin.admin_index'))
                else:
                    print "bad password"
            else:
                print "user mismatch"
        return self.render('admin/index.html', form=form)
    @expose('/logout')
    def logout(self):
        """Logout the current user."""
        user = current_user
        user.authenticated = False
        db.session.add(user)
        db.session.commit()
        logout_user()
        next = request.args.get('next')
        flash("You have successfully logged out")
        return redirect(url_for('admin.admin_index'))

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField, TextAreaField, SubmitField, validators
from wtforms.widgets import TextArea
from application.models import User
from flask_admin.contrib.sqla import ModelView

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])

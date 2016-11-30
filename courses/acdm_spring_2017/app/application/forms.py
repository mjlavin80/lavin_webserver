from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField, TextAreaField, SubmitField, validators
from application.models import User

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])

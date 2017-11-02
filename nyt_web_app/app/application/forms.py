from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField, TextAreaField, SubmitField, validators, widgets
from application.models import *
from wtforms_alchemy import ModelFieldList, model_form_factory
from wtforms.fields import FormField

ModelForm = model_form_factory(Form)

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])

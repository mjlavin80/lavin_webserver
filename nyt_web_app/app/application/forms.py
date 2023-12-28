from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField, validators, widgets
from application.models import *
from wtforms_alchemy import ModelFieldList, model_form_factory
from wtforms.fields import FormField

ModelForm = model_form_factory(Form)

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


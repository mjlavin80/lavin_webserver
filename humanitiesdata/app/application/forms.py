from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, SubmitField, SelectField, BooleanField, HiddenField, validators
#from wtforms.widgets import TextArea
from application.models import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask.ext.wtf import Form
from wtforms_alchemy import ModelFieldList, model_form_factory
from wtforms.fields import FormField
#from wtforms_alchemy import ModelForm

ModelForm = model_form_factory(Form)

class AddTag(ModelForm):
    class Meta:
        model = Tag

class AddResource(ModelForm):
    class Meta:
        model = Resource
        #recaptcha = RecaptchaField()
    tags = TextField(FormField(AddTag))

class SignupForm(ModelForm):
    class Meta:
        model = Signup

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])

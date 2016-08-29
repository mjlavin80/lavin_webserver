from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, SelectField, TextAreaField, SubmitField, validators
from application.models import User

"""
class Revision(Form):
    ocr = TextAreaField(description="revision_to_db")
    submit_draft = SubmitField("Submit Draft")
    submit_done = SubmitField("Submit Done")

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])
"""

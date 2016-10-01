from flask.ext.wtf import Form, RecaptchaField
from wtforms import TextField, PasswordField, SubmitField, SelectField, BooleanField, validators
from wtforms.widgets import TextArea
from application.models import User
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_admin.form.widgets import Select2Widget


class ApprovalQ(Form):
    approve = BooleanField()
    submit = SubmitField("Approve Selected")

class AddResource(Form):
    title = TextField(label='Title', validators=[validators.required()])
    description = TextField(label='Resource description', widget=TextArea(), validators=[validators.required()])
    uri = TextField(label='Resource URL', validators=[validators.required(message="Resource URL is required"), validators.URL(message="You must provide a URL endpoint for datasets and recipes")])
    submitted_by = TextField(label='Your Name', validators=[validators.required(message="Submitting a resource requires a name")])
    email = TextField(label='Email', validators=[validators.required(message="You must provide a valid email address to submit"), validators.Email(message="Submissions must include a valid email address")])
    resource_type = SelectField(label='Dataset or Recipe', choices=[("Dataset", "Dataset"), ("Recipe", "Recipe")])
    tags = TextField(label='Tag(s)', validators=[validators.required(message="At least one tag is required"), validators.Length(min=0, message=u'Please enter at least one tag or multiple tags separated by commas')])
    submit = SubmitField("Submit Resource")
    #recaptcha = RecaptchaField()

class AddTag(Form):
    tagname = TextField(label='Tag(s)', validators=[validators.required(), validators.Length(min=0, message=u'Enter tag of at least 1 characters or multiple tags separated by commas')])
    submit = SubmitField("Suggest one or More Tags")

class SignUp(Form):
    display_name = TextField(label='Name', validators=[validators.required(message="Name is required")])
    email = TextField(label='Email', validators=[validators.required(message="You must provide a valid email address to sign up"), validators.Email(message="Submissions must include a valid email address")])
    submit = SubmitField("Sign Up")

class LoginForm(Form):
    username = TextField('Username', [validators.required()])
    password = PasswordField('Password', [validators.required()])

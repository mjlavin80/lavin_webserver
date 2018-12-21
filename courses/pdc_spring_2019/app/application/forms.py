from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField, TextAreaField, SubmitField, validators, widgets
from application.models import *
from wtforms_alchemy import ModelFieldList, model_form_factory
from wtforms.fields import FormField
from wtforms.widgets import TextArea

ModelForm = model_form_factory(Form)

class CKEditor(TextArea):
    def __call__(self, field, **kwargs):
        c = kwargs.pop('class', '') or kwargs.pop('class_', '')
        kwargs['class'] = u'%s %s' % ('ckeditor', c)
        return super(CKEditor, self).__call__(field, **kwargs)

class CKEditorField(TextAreaField):
    widget = CKEditor()

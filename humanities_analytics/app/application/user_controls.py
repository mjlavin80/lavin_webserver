from flask import Flask, render_template, redirect, url_for, abort
from flask_login import current_user
from flask_admin.base import MenuLink
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from application import db
from application.models import *
from application.forms import CKEditor, CKEditorField
from urllib.parse import quote
from datetime import datetime


# AdminView
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        try:
            if current_user.is_authenticated() and current_user.is_approved():
                return self.render('admin/index.html')
            else: 
                return redirect(url_for('status'))
        except:
            return redirect(url_for('status'))

# Create menu links classes with reloaded accessible
class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_approved():
            return current_user.is_authenticated()

class ModelViewUserProfile(ModelView):
    column_exclude_list = ('custom_blog_path', 'is_admin', 'profile_image', 'approved', 'authenticated')
    form_excluded_columns = ('custom_blog_path', 'is_admin', 'profile_image', 'approved', 'authenticated')
    
    list_template = 'admin/model/custom_list.html'
    edit_template = 'admin/model/custom_edit.html'
    create_template = 'admin/model/custom_create.html'

    can_delete = False
    can_create = False

    form_widget_args = {
        'username': {
            'readonly': True
        },
    }

    #display only user's own content
    def is_owned(self, _id):
        model = db.session.query(self.model).filter(self.model.id == _id).one_or_none()
        if current_user.is_admin:
            return True
        if not model:
            return False
        try: 
            if model.username == current_user.username:
                return True
            else:
                return False
        except:
            return False
    
    def on_model_change(self, form, model, is_created):   
        if not self.is_owned(model.id):
            abort(403)
        try:
            if model.custom_blog_path == "" or model.custom_blog_path == None:
                if model.custom_blog_title != "":
                    model.custom_blog_path = quote(model.custom_blog_title.lower().replace(" ", "-"))
                else:
                    model.custom_blog_path = model.username
        except:
            pass

    def on_form_prefill(self, form, id):
        if not self.is_owned(id):
            abort(403)

    def on_model_delete(self, model):
        if not self.is_owned(model.id):
            abort(403)

    def get_query(self):
        if current_user.is_admin:
            return super(ModelViewUserProfile, self).get_query()
        else:
            return super(ModelViewUserProfile, self).get_query().filter(self.model.id == current_user.id)

    def get_count_query(self):
        if current_user.is_admin:
            return super(ModelViewUserProfile,self).get_count_query()
        else:
            return super(ModelViewUserProfile,self).get_count_query().filter(self.model.id == current_user.id)

    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_approved():
            return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))

class ModelViewUser(ModelView):
    column_exclude_list = ('lib_id', 'public')
    form_excluded_columns = ('lib_id', 'public')
    
    list_template = 'admin/model/custom_list.html'
    edit_template = 'admin/model/custom_edit.html'
    create_template = 'admin/model/custom_create.html'
    
    #display only user's own content
    def is_owned(self, _id):
        model = db.session.query(self.model).filter(self.model.id == _id).one_or_none()
        if current_user.is_admin:
            return True
        if not model:
            return False
        try: 
            if model.user_id == current_user.id:
                return True
            else:
                return False
        except:
            return False

    def on_model_change(self, form, model, is_created):   
        if not self.is_owned(model.id):
            abort(403)
        try:
            if model.public == "" or model.public == None:
                model.public = "True" 
        except:
            pass
        try:
            if model.user_id == "":
                model.user_id = current_user.id
        except:
            pass
        try:
            if model.post_path == "":
                model.post_path = quote(model.title.lower().replace(" ", "-")) 
        except:
            pass
        try:
            if not model.custom_blog_title:
                model.custom_blog_title = ""
        except:
            pass

    def on_form_prefill(self, form, id):
        if not self.is_owned(id):
            abort(403)

    def on_model_delete(self, model):
        if not self.is_owned(model.id):
            abort(403)

    def get_query(self):
        if current_user.is_admin:
        	return super(ModelViewUser, self).get_query()
        else:
        	return super(ModelViewUser, self).get_query().filter(self.model.user_id == current_user.id)

    def get_count_query(self):
        if current_user.is_admin:
        	return super(ModelViewUser,self).get_count_query()
        else:
        	return super(ModelViewUser,self).get_count_query().filter(self.model.user_id == current_user.id)

    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_approved():
            return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))

class ModelViewNotebook(ModelViewUser):
    column_hide_backrefs = False
    column_list = ('title', 'public', 'body', 'teaser','tags')
    form_overrides = dict(body=CKEditorField)
    form_columns = ('title', 'public', 'pub_date', 'teaser', 'body', 'tags')
    column_formatters = dict(body=lambda v, c, m, p: m.body[:100]+ " ...", teaser=lambda v, c, m, p: m.teaser[:25] if m.teaser else m.teaser)
    list_template = 'admin/model/custom_list.html'

    def on_model_change(self, form, model, is_created):
        model.pub_date = datetime.utcnow
        if not self.is_owned(model.id):
            abort(403)
        if model.user_id == "" or model.user_id == None or model.user_id == False:
            model.user_id = current_user.id
        if model.public == "" or model.public == None or model.public == False:
            model.public = "True"
        if model.post_path == "" or model.post_path == None or model.post_path == False:
            model.post_path = quote(model.title.lower().replace(" ", "-")) 

class ModelViewAdmin(ModelView):
    form_choices = { 'public': [ ("True", "True",), ("False", "False",)],}
    column_formatters = dict(course_description=lambda v, c, m, p: m.course_description[:100], office_hours=lambda v, c, m, p: m.office_hours[:100], 
        policies=lambda v, c, m, p: m.policies[:100], assignments=lambda v, c, m, p: m.assignments[:100], calendar=lambda v, c, m, p: m.calendar[:100])
    list_template = 'admin/model/custom_list.html'
    edit_template = 'admin/model/custom_edit.html'
    create_template = 'admin/model/custom_create.html'

    form_overrides = dict(course_description=CKEditorField, office_hours=CKEditorField, policies=CKEditorField, assignments=CKEditorField, calendar=CKEditorField)

    def on_model_change(self, form, model, is_created):
        try:
            if model.user_id == "":
                model.user_id = current_user.id
        except:
            pass
    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_admin:
            return current_user.is_authenticated()
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))

class ModelViewNotebookTag(ModelViewAdmin):
    column_hide_backrefs = False
    list_template = 'admin/model/custom_list.html'
    
    def on_model_change(self, form, model, is_created):   
        if model.public == "" or model.public == None or model.public == False:
            model.public = "True"
        if model.tag_path == "" or model.tag_path == None or model.tag_path == False:
            model.tag_path = quote(model.tag_name.lower().replace(" ", "-"))
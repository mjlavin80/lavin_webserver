from flask import Flask, render_template, redirect, url_for, abort
from flask_login import current_user
from flask_admin.base import MenuLink
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from application.forms import CKEditor, CKEditorField
from application import db
from application.models import *
from urllib.parse import quote
from datetime import datetime

#audit need for this function
def setkeys(d):
    try:
        d["date_submitted"] = d["date_submitted"].isoformat()
    except:
        pass
    del d["id"]
    del d["_sa_instance_state"]
    return d

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
        
class ModelViewAdmin(ModelView):
    form_choices = { 'public': [ ("True", "True",), ("False", "False",)],
                   }

    list_template = 'admin/model/custom_list.html'
    edit_template = 'admin/model/custom_edit.html'
    create_template = 'admin/model/custom_create.html'

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

class ModelViewTag(ModelViewAdmin):
    column_hide_backrefs = False
    column_list = ('public', 'tag_name',)
    form_columns = ('public', 'tag_name',)
    
    def on_model_change(self, form, model, is_created): 
        if model.tag_path == "" or model.tag_path == None:
            model.tag_path = quote(model.tag_name.lower().replace(" ", "-"))

class ModelViewResource(ModelViewAdmin):

    form_choices = { 'resource_type': [ ("dataset", "dataset",), ("recipe", "recipe",)],
                     'public': [ ("True", "True",), ("False", "False",)],
                   }
    form_overrides = dict(description=TextAreaField)

    order = ("public", "resource_type", "title", "description", "submitted_by", "email", 
        "access_url", "web_service", "modified", "publisher", "contact_point", "contact_email", 
        "identifier", "access_level", "access_level_comment", "bureau_code", "program_code", 
        "format_", "license", "rights", "spatial", "temporal", "collections", "tags")
    column_list = order
    form_columns = order

    def on_model_change(self, form, model, is_created):
        if model.public == "" or model.public == None:
                model.public = "True" 
        if model.date_submitted == "" or model.date_submitted == None:
            model.date_submitted = datetime.today()
        if model.excerpt == "" or model.excerpt == None:
            model.excerpt = "".join([" ".join(model.description.split(" ")[:9]), " ..."])
    
    def after_model_change(self, form, model, is_created):
        more_link = "".join(["<a href='/resources/", str(model.id), "'>Full Record</a>"])
        print(more_link)
        if model.more_link != more_link:
            model.more_link = more_link
            db.session.commit()
            
class ModelViewCollection(ModelViewAdmin):
    order = ("public", "title", "description", "items")
    form_overrides = dict(description=CKEditorField)
    column_list = order
    form_columns = order
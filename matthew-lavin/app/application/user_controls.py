from flask import Flask, render_template, redirect, url_for, abort
from flask_login import current_user
from flask_admin.base import MenuLink
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from application.forms import CKEditor, CKEditorField
from wtforms import TextAreaField
from application import db
from urllib.parse import quote

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

    form_overrides = dict(entry_blurb=TextAreaField, entry_essay=CKEditorField)
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

class ModelViewBlog(ModelViewUser):
    column_hide_backrefs = False
    column_list = ('title', 'body', 'teaser','tags')
    form_overrides = dict(body=CKEditorField)
    form_columns = ('title', 'pub_date', 'teaser', 'body', 'tags')
    column_formatters = dict(body=lambda v, c, m, p: m.body[:100]+ " ...", teaser=lambda v, c, m, p: m.teaser[:25]+" ..." if m.teaser else m.teaser)
    
    def on_model_change(self, form, model, is_created):
        if model.public == "" or model.public == None:
            model.public = "True" 
        if model.post_path == "" or model.post_path == None:
            model.post_path = quote(model.title.lower().replace(" ", "-")) 
        if model.user_id == "" or model.user_id == None:
            model.user_id = current_user.id

class ModelViewTag(ModelViewUser):
    column_hide_backrefs = False
    column_list = ('tag_name',)
    form_columns = ('tag_name',)
    can_delete = False
    can_edit = False
    def on_model_change(self, form, model, is_created):
        if model.public == "" or model.public == None:
                model.public = "True" 
        if model.tag_path == "" or model.tag_path == None:
            model.tag_path = quote(model.tag_name.lower().replace(" ", "-"))
        
class ModelViewAdmin(ModelView):
    form_excluded_columns = ('custom_blog_path')
    column_formatters = dict(course_description=lambda v, c, m, p: m.course_description[:25]+ " ...", description=lambda v, c, m, p: m.description[:25]+ " ...")
    form_overrides = dict(description=TextAreaField, course_description=TextAreaField)
    form_widget_args = dict(description=dict(rows=10), course_description=dict(rows=10))
    
    def on_model_change(self, form, model, is_created):
        try:
            if not model.custom_blog_title:
                model.custom_blog_title = ""
        except:
            pass
        try:
            if model.user_id == "":
                model.user_id = current_user.id
        except:
            pass
        try:
            if model.custom_blog_path == "" or model.custom_blog_path == None:
                if model.custom_blog_title != "":
                    model.custom_blog_path = quote(model.custom_blog_title.lower().replace(" ", "-"))
                else:
                    model.custom_blog_path = model.username
        except:
            pass
        try:
            if model.post_path == "":
               model.post_path = quote(model.title.lower().replace(" ", "-")) 
        except:
            pass
        
    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_admin:
            return current_user.is_authenticated()
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))
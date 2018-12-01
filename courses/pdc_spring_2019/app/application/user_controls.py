from flask import Flask, render_template, redirect, url_for, send_from_directory, request, flash, g, session
from flask_login import current_user
from flask_admin.base import MenuLink
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import TextAreaField
from application.forms import CKEditor, CKEditorField
from application import db

# AdminView
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        try:
            current_user.is_authenticated() == True
            return self.render('admin/index.html')
        except:
            return redirect(url_for('status', message="unauthorized"))

# Create menu links classes with reloaded accessible
class AuthenticatedMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated()

class ModelViewUser(ModelView):
    column_exclude_list = ('lib_id', 'public', 'custom_blog_path')
    form_excluded_columns = ('lib_id', 'public', 'custom_blog_path')
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
        if model.user_id == current_user.id:
            return True
        else:
        	return False
    
    def on_model_change(self, form, model, is_created):
        if not self.is_owned(model.id):
            abort(403)
        if not model.custom_blog_path:
            if model.custom_blog_title:
                model.custom_blog_path = quote(custom_blog_title.lower().replace(" ", "-"))
            else:
                model.custom_blog_path = model.id

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

    def on_model_change(self, form, model, is_created):
        model.user_id = current_user.id
        if not model.public:
            model.public = True

    def is_accessible(self):
        if current_user.is_authenticated():
            return current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))

class ModelViewBlog(ModelViewUser):
    column_hide_backrefs = False
    column_list = ('title', 'body', 'tags')
    form_overrides = dict(body=CKEditorField)
    form_columns = ('title', 'pub_date', 'body', 'tags')

class ModelViewTag(ModelViewUser):
    column_hide_backrefs = False
    column_list = ('tag_name',)
    form_columns = ('tag_name',)

class ModelViewAdmin(ModelView):
    form_excluded_columns = ('custom_blog_path')
    column_formatters = dict(course_description=lambda v, c, m, p: m.course_description[:25]+ " ...", description=lambda v, c, m, p: m.description[:25]+ " ...")
    form_overrides = dict(description=TextAreaField, course_description=TextAreaField)
    form_widget_args = dict(description=dict(rows=10), course_description=dict(rows=10))
    
    def on_model_change(self, form, model, is_created):
        if not model.user_id:
            model.user_id = current_user.id
        if not model.custom_blog_path:
            if model.custom_blog_title:
                model.custom_blog_path = quote(custom_blog_title.lower().replace(" ", "-"))
            else:
                model.custom_blog_path = model.id

    def is_accessible(self):
        if current_user.is_authenticated() and current_user.is_admin:
            return current_user.is_authenticated()
    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('status'))

# custom view for readings
class ReadingViewAdmin(ModelViewAdmin):
    column_filters = ('last_name', 'public', 'link')

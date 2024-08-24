from application import db
from wtforms import fields, widgets
from datetime import datetime

# Define wtforms widget and field
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()

class GithubToken(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(250), index=True, unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_approved(self):
        """Return True if the user is authenticated."""
        return self.approved

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    public = db.Column(db.String(128), nullable=False)
    resource_type = db.Column(db.String(128), index=True, nullable=False)
    title = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    excerpt = db.Column(db.String(128))
    more_link = db.Column(db.String(128))
    submitted_by = db.Column(db.String(128), index=True, nullable=False)
    email = db.Column(db.String(128), index=True, nullable=False)
    access_url = db.Column(db.String(128), index=True, unique=True)
    web_service = db.Column(db.String(128), index=True, info={'label': 'Endpoint'})
    modified = db.Column(db.String(128))
    publisher = db.Column(db.String(128), index=True)
    contact_point = db.Column(db.String(128), index=True)
    contact_email = db.Column(db.String(128), index=True)
    identifier = db.Column(db.String(128), index=True)
    access_level = db.Column(db.String(128), index=True)
    access_level_comment = db.Column(db.String(2000))
    bureau_code = db.Column(db.String(128), index=True)
    program_code = db.Column(db.String(128), index=True)
    format_ = db.Column(db.String(128), index=True)
    license = db.Column(db.String(128), index=True)
    rights = db.Column(db.String(128), index=True)
    spatial = db.Column(db.String(128), index=True)
    temporal = db.Column(db.String(128), index=True)
    date_submitted = db.Column(db.DateTime, default=datetime.today())
    
    tags = db.relationship('TagsResources', back_populates='resources', lazy='joined')
    collections = db.relationship('CollectionItems', back_populates='resources')

    def __repr__(self):
        return '<Resource %r>' % self.title


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer(), primary_key=True)
    public = db.Column(db.String(128), nullable=False)
    tag_name = db.Column(db.String(500), nullable=False)
    tag_path = db.Column(db.String(500), nullable=False)
    resources = db.relationship('TagsResources', back_populates='tags')

    def __repr__(self):
        return '<Tag %r >' % self.tag_name

class Collection(db.Model):
    __tablename__ = 'collection'

    id = db.Column(db.Integer, primary_key=True)
    public = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(999), nullable=False)
    description = db.Column(db.String(2000)) 
    items = db.relationship('CollectionItems', back_populates='collections')

    def __repr__(self):
        return '<Collection %r >' % self.title

class CollectionItems(db.Model):
    __tablename__='collection_items'

    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id', ondelete='CASCADE'), nullable=False)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id', ondelete='CASCADE'), nullable=False)
    collection_title = db.Column(db.String(128))
    resource_title = db.Column(db.String(128))
    order = db.Column(db.Integer)

    collections = db.relationship('Collection', back_populates='items')
    resources =  db.relationship('Resource', back_populates='collections')

class TagsResources(db.Model):
    __tablename__='tags_resources'

    id = db.Column(db.Integer(), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id', ondelete='CASCADE'))
    resource_id = db.Column(db.Integer(), db.ForeignKey('resource.id', ondelete='CASCADE'))
    tags = db.relationship('Tag', back_populates='resources')
    resources =  db.relationship('Resource', back_populates='tags')


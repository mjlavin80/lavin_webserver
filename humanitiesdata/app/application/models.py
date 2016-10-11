from application import db
from dictalchemy import DictableModel
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy_utils import EmailType

Base = declarative_base(cls=DictableModel)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(128), index=True)
    display_name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(512))
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'))
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(128), index=True, unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.tagname

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(2000), nullable=False)
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
    resource_type = db.Column(db.String(128), index=True)
    status = db.Column(db.String(128), index=True)
    date_submitted = db.Column(db.DateTime)
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('resources', lazy='dynamic'))

    def __repr__(self):
        return '<Resource %r>' % self.title

class Signup(db.Model):
    __tablename__ = "signup"
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(128), index=True, unique=True, nullable=False)
    email = db.Column(EmailType, index=True, unique=True, nullable=False)
    comments = db.Column(db.String(2000))
    date = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return '<Email %r>' % self.email

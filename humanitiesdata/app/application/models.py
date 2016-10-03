from application import db
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(128), index=True, unique=False)
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
    title = db.Column(db.String(128), index=True)
    description = db.Column(db.String(512), index=True)
    uri = db.Column(db.String(128), index=True)
    submitted_by = db.Column(db.String(128), index=True)
    email = db.Column(db.String(128), index=True)
    dateSubmitted = db.Column(db.DateTime)
    modified = db.Column(db.String(128))
    publisher = db.Column(db.String(512), index=True)
    contactPoint = db.Column(db.String(128), index=True)
    identifier = db.Column(db.String(128), index=True)
    accessLevel = db.Column(db.String(128), index=True)
    bureauCode = db.Column(db.String(128), index=True)
    license = db.Column(db.String(128), index=True)
    rights = db.Column(db.String(128), index=True)
    spatial = db.Column(db.String(128), index=True)
    temporal = db.Column(db.String(128), index=True)
    resource_type = db.Column(db.String(128), index=True) #only dataset and recipe?
    status = db.Column(db.String(128), index=True)
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('resources', lazy='dynamic'))

    def __repr__(self):
        return '<Resource %r>' % self.uri

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Email %r>' % self.email

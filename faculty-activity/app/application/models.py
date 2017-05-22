from application import db
from datetime import datetime

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

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sort_order = db.Column(db.Integer)
    title = db.Column(db.String(128))
    description = db.Column(db.String(9999))
    date = db.Column(db.String(128))

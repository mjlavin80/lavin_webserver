from application import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(128), index=True, unique=False)
    display_name = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(50))
    authenticated = db.Column(db.Boolean, default=False)

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

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), index=True)
    description = db.Column(db.String(512), index=True)
    uri = db.Column(db.String(50), index=True)
    submitted_by = db.Column(db.String(50), index=True)
    email = db.Column(db.String(50), index=True, unique=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Resource %r>' % self.uri

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagname = db.Column(db.String(50), index=True, unique=True)

    def __repr__(self):
        return '<Resource %r>' % self.tagname

class Resource_Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'))

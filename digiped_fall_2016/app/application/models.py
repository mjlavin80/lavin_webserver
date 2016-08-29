from application import db

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True, unique=False)
    stub = db.Column(db.String(128), index=True, unique=False)

    def __repr__(self):
        return '<Work %r>' % self.stub

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(512), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(512), index=True, unique=False)
    display_name = db.Column(db.String(512), index=True, unique=True)
    email = db.Column(db.String(512), index=True, unique=True)
    password = db.Column(db.String(512))
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

class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('work.id'))
    image_uri = db.Column(db.String(128), index=True, unique=False)
    ocr_text = db.Column(db.String(9999), index=False, unique=False)
    status = db.Column(db.Integer) #0,1,2,3,4

    def __repr__(self):
        return '<Node %r>' % self.id, self.status

class Revisions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    datetime = db.Column(db.String(128), index=True, unique=False)
    text = db.Column(db.String(9999), index=False, unique=False)

    def __repr__(self):
        return '<Revisions %r>' % self.id

#combine with revisions, add type column
class Verifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    node_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    datetime = db.Column(db.String(128), index=True, unique=False)
    text = db.Column(db.String(9999), index=False, unique=False)

    def __repr__(self):
        return '<Verifications %r>' % self.id

class Instructions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_ids = db.Column(db.String(256), index=True, unique=False)
    node_ids = db.Column(db.String(256), index=True, unique=False)
    rule_text = db.Column(db.String(1024), index=False, unique=False)
    def __repr__(self):
        return '<Instructions %r>' % self.id, self.rule_text

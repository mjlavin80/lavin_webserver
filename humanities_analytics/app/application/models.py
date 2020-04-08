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

class StaticPage(db.Model):
    __tablename__="static_page"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), default="True")
    title = db.Column(db.String(500), nullable=False)
    route = db.Column(db.String(512), nullable=False)
    page_data = db.Column(db.Text(), nullable=False)

class Syllabus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), default="True")
    course = db.Column(db.String(512), nullable=False)
    semester = db.Column(db.String(512), nullable=False)
    course_description = db.Column(db.Text(), nullable=False)
    office_hours= db.Column(db.Text(), nullable=False)
    policies = db.Column(db.Text(), nullable=False)
    assignments = db.Column(db.Text(), nullable=False)
    calendar = db.Column(db.Text(), nullable=False)
    instructor = db.Column(db.String(512), nullable=False)
    email = db.Column(db.String(512), nullable=False)
    office = db.Column(db.String(512), nullable=False)
    office_hours_brief = db.Column(db.String(512), nullable=False)
    classroom = db.Column(db.String(512), nullable=False)
    meeting_time = db.Column(db.String(512), nullable=False)
    lab_time = db.Column(db.String(512), nullable=False)

class NotebookPost(db.Model):
    __tablename__="notebook_post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), default="True")
    title = db.Column(db.String(500), nullable=False)
    post_path = db.Column(db.String(512), default="")
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teaser = db.Column(db.String(512))
    body = db.Column(db.Text(), nullable=False)
    tags = db.relationship('NotebookTag', secondary="notebook_tags_posts", backref=db.backref('notebook_tags', 
        lazy='dynamic'))
    def __repr__(self):
        return '<Notebook Post %r >' % self.title

class NotebookTag(db.Model):
    __tablename__="notebook_tag"
    id = db.Column(db.Integer(), primary_key=True)
    tag_name = db.Column(db.String(500), nullable=False)
    tag_path = db.Column(db.String(500), default="")
    public = db.Column(db.String(128), default="True")

    def __repr__(self):
        return '<Notebook Tag %r >' % self.tag_name

class NotebookTagsPosts(db.Model):
    __tablename__="notebook_tags_posts"
    id = db.Column(db.Integer(), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey('notebook_tag.id', ondelete='CASCADE'))
    blog_post_id = db.Column(db.Integer(), db.ForeignKey('notebook_post.id', ondelete='CASCADE'))
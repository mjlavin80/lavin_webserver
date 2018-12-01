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
    profile_image = db.Column(db.String(250), index=True, unique=False)
    display_name = db.Column(db.String(250), index=True, unique=True)
    email = db.Column(db.String(250), index=True, unique=True)
    authenticated = db.Column(db.Boolean, default=False)
    custom_blog_title = db.Column(db.Text(), default="", nullable=True)
    custom_blog_path = db.Column(db.String(512), nullable=False)
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

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    assignments = db.relationship('Assignment', backref='day', lazy='joined')
    readings = db.relationship('Reading', backref='day', lazy='joined')
    activities = db.relationship('Activity', backref='day', lazy='joined')
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'))

    def __repr__(self):
        return '<Day %r %r >' % (self.id, self.name)

class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week_number = db.Column(db.Integer)
    week_topic = db.Column(db.String(128))
    days = db.relationship('Day', backref='week', lazy='joined')
    def __repr__(self):
        return '<Week %r %r >' % (self.week_number, self.week_topic)

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128))
    title = db.Column(db.String(128))
    description = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128))
    title = db.Column(db.String(128), nullable=False)
    submit_instructions = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128))
    description = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)
    link_title = db.Column(db.String(128))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    text_date = db.Column(db.String(128))
    def __repr__(self):
        return '<Assignment %r %r>' % (self.id, self.title)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    page_range = db.Column(db.String(50))
    publisher = db.Column(db.String(50))
    pubdate = db.Column(db.String(50))
    pubplace = db.Column(db.String(50))
    link = db.Column(db.String(128))
    article_title = db.Column(db.String(128))
    book_title = db.Column(db.String(128))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Reading %r %r >' % (self.last_name, self.article_title)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)
    order = db.Column(db.String(100))
    link = db.Column(db.String(500))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Activity %r %r >' % (self.link, self.title)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    lib_id = db.Column(db.String(128))
    public = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    field_notes = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)
    
    def __repr__(self):
        return '<Dataset %r >' % self.title

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    title = db.Column(db.Text(), nullable=False)
    public = db.Column(db.String(128), nullable=False)

class CollectionItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)
    target_table = db.Column(db.String(200), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.String(100), nullable=False)

class TimelineEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), nullable=False)
    headline = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    end_year = db.Column(db.Integer)
    end_month = db.Column(db.Integer)
    end_day = db.Column(db.Integer)
    display_date = db.Column(db.String(128))
    media = db.Column(db.String(500))
    media_credit = db.Column(db.String(128))   
    media_caption = db.Column(db.String(500))
    media_thumbnail = db.Column(db.String(500))
    entry_type = db.Column(db.String(128))
    entry_group = db.Column(db.String(128))
    background = db.Column(db.String(128))
    entry_teaser = db.Column(db.Text(), info={'widget': CKTextAreaWidget()}, nullable=False)
    entry_essay = db.Column(db.Text(), info={'widget': CKTextAreaWidget()}, nullable=False)

    def __repr__(self):
        return '<Timeline Entry %r >' % self.headline

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    post_path = db.Column(db.String(512), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teaser = db.Column(db.String(512))
    body = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)
    tags = db.relationship('Tag', secondary="tags_posts", backref=db.backref('tags', 
        lazy='dynamic'))
    def __repr__(self):
        return '<Blog Post %r >' % self.title

class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tag_name = db.Column(db.String(500), nullable=False)
    public = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Tag %r >' % self.tag_name

class TagsPosts(db.Model):
    __tablename__="tags_posts"
    id = db.Column(db.Integer(), primary_key=True)
    tag_id = db.Column(db.Integer(), db.ForeignKey('tag.id', ondelete='CASCADE'))
    blog_post_id = db.Column(db.Integer(), db.ForeignKey('blog_post.id', ondelete='CASCADE'))

class Basics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    instructor = db.Column(db.String(128))
    office = db.Column(db.String(128))
    office_hours = db.Column(db.String(128))
    email = db.Column(db.String(128))
    zotero = db.Column(db.String(500))
    github = db.Column(db.String(500))
    hypoth = db.Column(db.String(500))
    course_name = db.Column(db.String(500))
    course_description = db.Column(db.Text(),info={'widget': CKTextAreaWidget()}, nullable=False)
    semester_year = db.Column(db.String(128))
    department = db.Column(db.String(128))
    institution = db.Column(db.String(128))

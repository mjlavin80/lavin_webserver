from application import db
from wtforms import fields, widgets

# Define wtforms widget and field
class CKTextAreaWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('class_', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(fields.TextAreaField):
    widget = CKTextAreaWidget()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))

class GithubToken(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    github_access_token = db.Column(db.String(200))

    def __init__(self, github_access_token):
        self.github_access_token = github_access_token

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), index=True, unique=True)
    is_admin = db.Column(db.Boolean, default=True)
    profile_image = db.Column(db.String(250), index=True, unique=False)
    display_name = db.Column(db.String(250), index=True, unique=True)
    email = db.Column(db.String(250), index=True, unique=True)
    password = db.Column(db.String(500))
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

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nyt_id = db.Column(db.String(99))
    review_type = db.Column(db.String(500))
    month = db.Column(db.String(99))
    year = db.Column(db.String(99))
    document_type = db.Column(db.String(250))
    headline = db.Column(db.String(500))
    byline = db.Column(db.String(500))
    page = db.Column(db.String(500))
    pub_date = db.Column(db.String(500))
    word_count = db.Column(db.String(99))
    review_word_count = db.Column(db.Integer)
    ocr_transcription = db.Column(db.String(99999))
    corrected_transcription = db.Column(db.String(99999))
    perceived_author_name = db.Column(db.String(99))
    perceived_author_gender = db.Column(db.String(99))
    reviewed_work_title = db.Column(db.String(500))
    nyt_pdf_endpoint = db.Column(db.String(500))
    reviewed_work = db.Column(db.Integer, db.ForeignKey('work.id'))
    cluster_meta_children = db.relationship('ClusterMeta', backref='cluster_meta_children', lazy='joined')

    def __repr__(self):
        return 'Review %r' % (self.nyt_id,)

class ClusterMeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_cluster = db.Column(db.Integer, db.ForeignKey('metadata.id'))
    nyt_id = db.Column(db.String(99))
    review_type = db.Column(db.String(500))
    corrected_transcription = db.Column(db.String(99999))
    perceived_author_name = db.Column(db.String(99))
    perceived_author_gender = db.Column(db.String(99))
    
    def __repr__(self):
        return 'Cluster from %r - %r' % (self.nyt_id , self.id)

class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viaf_uri = db.Column(db.String(500))
    title = db.Column(db.String(500))
    publisher = db.Column(db.String(99))
    price = db.Column(db.String(99))
    edition_notes = db.Column(db.String(500))
    edition_format = db.Column(db.String(99))
    pub_date = db.Column(db.String(99))
    genre = db.Column(db.String(500))
    subgenre = db.Column(db.String(500))
    author = db.Column(db.Integer, db.ForeignKey('author.id'))
    reviews = db.relationship('Metadata', backref='metadata_work', lazy='joined')

    def __repr__(self):
        return 'Work %r %r' % (self.id, self.title)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viaf_uri = db.Column(db.String(500))
    last_name = db.Column(db.String(99))
    first_name = db.Column(db.String(99))
    common_name = db.Column(db.String(99))
    gender = db.Column(db.String(99))
    year_of_birth = db.Column(db.String(99))
    year_of_death = db.Column(db.String(99))
    works = db.relationship('Work', backref='author_works', lazy='joined')

    def __repr__(self):
        return 'Author %r %r %r' % (self.id, self.last_name, self.first_name)

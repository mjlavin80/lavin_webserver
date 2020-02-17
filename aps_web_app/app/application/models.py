from application import db
from datetime import datetime

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
    custom_blog_title = db.Column(db.String(1224), nullable=True)
    custom_blog_path = db.Column(db.String(512), default="")
    custom_blog_description = db.Column(db.Text(), default="")
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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    public = db.Column(db.String(128), default="True")
    title = db.Column(db.String(500), nullable=False)
    route = db.Column(db.String(512), nullable=False)
    page_data = db.Column(db.Text(), nullable=False)
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String(512), index=True)
    source_type = db.Column(db.String(512), index=True)
    language_code = db.Column(db.String(128), index=False)
    eissn = db.Column(db.String(128), index=False)
    action_code = db.Column(db.String(128), index=False)
    record_id = db.Column(db.String(128), index=False)
    start_page = db.Column(db.String(128), index=False) 
    issn = db.Column(db.String(128), index=False)
    volume = db.Column(db.String(128), index=False)
    publisher = db.Column(db.String(512), index=False) 
    date_time_stamp = db.Column(db.String(128), index=False)
    full_text = db.Column(db.Text())
    alpha_pub_date = db.Column(db.String(128), index=False)
    numeric_pub_date = db.Column(db.Integer)
    version = db.Column(db.String(128), index=False)
    abstract = db.Column(db.Text())
    record_title = db.Column(db.String(128), index=False)
    issue = db.Column(db.String(128), index=False)
    pagination = db.Column(db.String(128), index=False)
    url_doc_view = db.Column(db.String(128), index=False)
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    contrib_id = db.Column(db.Integer, db.ForeignKey('contributor.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'))
    last_edited = db.Column(db.String(128), index=False)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    status = db.Column(db.String(128), index=True)
    review_type = db.Column(db.String(256), index=False)
    reviewed_book_title = db.Column(db.String(256), index=False)
    reviewed_book_pub_date = db.Column(db.String(256), index=False)
    reviewed_book_publisher = db.Column(db.String(256), index=False)
    reviewed_book_publisher_viaf_match = db.Column(db.String(256), index=False)
    reviewed_book_genre = db.Column(db.String(256), index=False)
    reviewed_book_price = db.Column(db.String(256), index=False)
    reviewed_author_viaf_match = db.Column(db.String(256), index=False)
    reviewed_author_name = db.Column(db.String(99))
    perceived_author_gender = db.Column(db.String(99))
    pub = db.relationship('Publication', backref=db.backref('associated_articles', lazy='dynamic'))
    contributor = db.relationship('Contributor', backref=db.backref('also_by_this_contributor', lazy='dynamic'))

class Contributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization_name = db.Column(db.String(128), index=False)
    first_name = db.Column(db.String(128), index=False)
    middle_name = db.Column(db.String(128), index=False)
    last_name = db.Column(db.String(128), index=False)
    person_name = db.Column(db.String(128), index=False)
    person_title = db.Column(db.String(128), index=False)
    name_suffix = db.Column(db.String(128), index=False)
    role = db.Column(db.String(128), index=False)
    original_form = db.Column(db.String(256), index=False)

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=False)
    qualifier = db.Column(db.String(128), index=False)
    
class ExtractedParsed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'))
    review_type = db.Column(db.String(256), index=False)
    reviewed_book_title = db.Column(db.String(256), index=False)
    reviewed_book_pub_date = db.Column(db.String(256), index=False)
    reviewed_book_publisher = db.Column(db.String(256), index=False)
    reviewed_book_publisher_viaf_match = db.Column(db.String(256), index=False)
    reviewed_book_genre = db.Column(db.String(256), index=False)
    reviewed_book_price = db.Column(db.String(256), index=False)
    reviewed_author_viaf_match = db.Column(db.String(256), index=False)
    reviewed_author_name = db.Column(db.String(256), index=False)
    perceived_author_gender = db.Column(db.String(128), index=False)
    experiment = db.Column(db.String(256), index=False)
    annotation = db.Column(db.String(512), index=False)
    date_time = db.Column(db.String(256), index=False)
    
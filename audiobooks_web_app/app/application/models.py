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

class Main(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	asin = db.Column(db.String(128))
	uri = db.Column(db.String(512))      
	date_scraped = db.Column(db.DateTime, index=True, default=datetime.today())
	scrape_method = db.Column(db.String(128), index=True) # controlled vocab in form choices
	author_count = db.Column(db.Integer, index=True)
	narrator_count = db.Column(db.Integer, index=True)
	title = db.Column(db.String(512), index=True, nullable=False) 
	subtitle = db.Column(db.String(512)) 
	cover_image_uri = db.Column(db.String(512)) 
	language = db.Column(db.String(128), index=True)
	copyright = db.Column(db.String(128), index=True)
	extended_product_description = db.Column(db.String(2048))
	is_pdf_url_available = db.Column(db.Integer) # true false
	isbn = db.Column(db.Integer) 
	product_site_launch_date = db.Column(db.String(128), index=True)
	read_along_support = db.Column(db.Integer) # true false
	merchandising_description = db.Column(db.String(2048))
	merchandising_summary = db.Column(db.String(2048))
	content_delivery_type = db.Column(db.String(128), index=True) 
	content_type = db.Column(db.String(128), index=True)   
	format_type = db.Column(db.String(128), index=True)   
	has_children = db.Column(db.Boolean) # true false   
	is_adult_product = db.Column(db.Boolean) # true false    
	is_listenable = db.Column(db.Boolean) # true false  
	is_buyable = db.Column(db.Boolean) # true false
	is_preorderable = db.Column(db.Boolean) # true false
	is_purchasability_suppressed = db.Column(db.Boolean) # true false
	is_vvab = db.Column(db.Boolean) # true false
	is_world_rights = db.Column(db.Boolean) # true false
	issue_date = db.Column(db.DateTime, index=True)  
	release_date = db.Column(db.DateTime, index=True)    
	publisher_name = db.Column(db.String(128), index=True)   
	publisher_summary = db.Column(db.String(2048)) 
	publisher_uri = db.Column(db.String(512))
	series_name = db.Column(db.String(128), index=True)  
	series_uri = db.Column(db.String(512))    
	runtime_length_min = db.Column(db.Integer) 
	sample_url = db.Column(db.String(512))   
	sku =  db.Column(db.String(128), index=True)   
	sku_lite = db.Column(db.String(128), index=True) 
	platinum_keywords = db.Column(db.String(2048))
	authors = db.relationship('Author', secondary='main_author', backref=db.backref('authors', 
        lazy='dynamic'))
	narrators = db.relationship('Narrator', secondary='main_narrator', backref=db.backref('narrators', 
        lazy='dynamic'))
	genres = db.relationship('Genre', secondary='main_genre', backref=db.backref('genres', 
        lazy='dynamic'))
	subgenres = db.relationship('Subgenre', secondary='main_subgenre', backref=db.backref('subgenres', 
        lazy='dynamic'))

class FullReview(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	main_id = db.Column(db.Integer(), db.ForeignKey('main._id', ondelete='CASCADE'))
	date_scraped = db.Column(db.DateTime, index=True, default=datetime.today()) 
	main_asin = db.Column(db.String(128))
	audible_id = db.Column(db.String(128))
	author_id = db.Column(db.String(512))
	author_name = db.Column(db.String(512), index=True)
	title = db.Column(db.String(512), index=True)
	body = db.Column(db.String(2048))
	format = db.Column(db.String(128), index=True)
	location = db.Column(db.String(128), index=True)
	submission_date = db.Column(db.DateTime, index=True) 
	overall_rating = db.Column(db.Integer)
	performance_rating = db.Column(db.Integer)
	story_rating = db.Column(db.Integer)
	content_quality_score = db.Column(db.Integer)
	num_helpful_votes = db.Column(db.Integer)
	num_unhelpful_votes = db.Column(db.Integer)

class GuidedResponse(db.Model):
	_id = db.Column(db.Integer, primary_key=True)
	review_id = db.Column(db.Integer(), db.ForeignKey('full_review._id', ondelete='CASCADE'))
	date_scraped = db.Column(db.DateTime, index=True, default=datetime.today()) 
	audible_id = db.Column(db.String(128))
	question = db.Column(db.String(512), index=True)
	question_type = db.Column(db.String(128), index=True)
	answer = db.Column(db.String(2048))
    
class Author(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(128))
    name = db.Column(db.String(128), index = True) #can be list, other known name
    uri = db.Column(db.String(512)) 
    bio = db.Column(db.String(2048)) 

class Narrator(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index = True) 
    
class Genre(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    audible_id = db.Column(db.String(128)) 
    name = db.Column(db.String(128), index = True) 
    
class Subgenre(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    audible_id = db.Column(db.String(128))
    name = db.Column(db.String(128), index = True) 
    genre_id = db.Column(db.Integer(), db.ForeignKey('genre._id', ondelete='CASCADE'))

class PriceReviews(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    main_id=db.Column(db.Integer, db.ForeignKey('main._id'), nullable=False)
    date_scraped = db.Column(db.DateTime, index=True, default=datetime.today())
    price=db.Column(db.Float, index=True)
    price_unit=db.Column(db.String(128), index=True)
    num_reviews=db.Column(db.Integer, index=True)
    overall_average_rating=db.Column(db.Float, index=True)
    overall_display_average_rating=db.Column(db.Float, index=True)
    overall_display_stars=db.Column(db.Float, index=True)
    overall_num_five_star_ratings=db.Column(db.Float, index=True)
    overall_num_four_star_ratings=db.Column(db.Float, index=True)
    overall_num_three_star_ratings=db.Column(db.Float, index=True)
    overall_num_two_star_ratings=db.Column(db.Float, index=True)
    overall_num_one_star_ratings=db.Column(db.Float, index=True)
    overall_num_ratings=db.Column(db.Float, index=True)
    performance_average_rating=db.Column(db.Float, index=True)
    performance_display_average_rating=db.Column(db.Float, index=True)
    performance_display_stars=db.Column(db.Float, index=True)
    performance_num_five_star_ratings=db.Column(db.Integer, index=True)
    performance_num_four_star_ratings=db.Column(db.Integer, index=True)
    performance_num_three_star_ratings=db.Column(db.Integer, index=True)
    performance_num_two_star_ratings=db.Column(db.Integer, index=True)
    performance_num_one_star_ratings=db.Column(db.Integer, index=True)
    performance_num_ratings=db.Column(db.Integer, index=True)
    story_average_rating=db.Column(db.Float, index=True)
    story_display_average_rating=db.Column(db.Float, index=True)
    story_display_stars=db.Column(db.Float, index=True)
    story_num_five_star_ratings=db.Column(db.Integer, index=True)
    story_num_four_star_ratings=db.Column(db.Integer, index=True)
    story_num_three_star_ratings=db.Column(db.Integer, index=True)
    story_num_two_star_ratings=db.Column(db.Integer, index=True)
    story_num_one_star_ratings=db.Column(db.Integer, index=True)
    story_num_ratings=db.Column(db.Integer, index=True)

class MainAuthor(db.Model):
    __tablename__="main_author"
    _id = db.Column(db.Integer(), primary_key=True)
    main_id = db.Column(db.Integer(), db.ForeignKey('main._id', ondelete='CASCADE'))
    author_id = db.Column(db.Integer(), db.ForeignKey('author._id', ondelete='CASCADE'))
    
class MainNarrator(db.Model):
    __tablename__="main_narrator"
    _id = db.Column(db.Integer(), primary_key=True)
    main_id = db.Column(db.Integer(), db.ForeignKey('main._id', ondelete='CASCADE'))
    narrator_id = db.Column(db.Integer(), db.ForeignKey('narrator._id', ondelete='CASCADE'))

class MainGenre(db.Model):
    __tablename__="main_genre"
    _id = db.Column(db.Integer(), primary_key=True)
    main_id = db.Column(db.Integer(), db.ForeignKey('main._id', ondelete='CASCADE'))
    genre_id = db.Column(db.Integer(), db.ForeignKey('genre._id', ondelete='CASCADE'))

class MainSubgenre(db.Model):
    __tablename__="main_subgenre"
    _id = db.Column(db.Integer(), primary_key=True)
    main_id = db.Column(db.Integer(), db.ForeignKey('main._id', ondelete='CASCADE'))
    subgenre_id = db.Column(db.Integer(), db.ForeignKey('subgenre._id', ondelete='CASCADE'))

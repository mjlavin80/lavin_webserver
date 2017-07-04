from application import db

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

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    submit_instructions = db.Column(db.String(128))
    slug = db.Column(db.String(128))
    description = db.Column(db.String(9999))
    link_title = db.Column(db.String(128))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))
    text_date = db.Column(db.String(128))
    def __repr__(self):
        return '<Assignment %r %r>' % (self.id, self.title)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    description = db.Column(db.String(9999))

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.String(100))
    link = db.Column(db.String(500))
    description = db.Column(db.String(9999))
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'))

    def __repr__(self):
        return '<Activity %r %r >' % (self.link, self.description)

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Basics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor = db.Column(db.String(128))
    office = db.Column(db.String(128))
    office_hours = db.Column(db.String(128))
    email = db.Column(db.String(128))
    zotero = db.Column(db.String(500))
    github = db.Column(db.String(500))
    hypoth = db.Column(db.String(500))
    course_name = db.Column(db.String(512))
    course_description = db.Column(db.String(9999))
    semester_year = db.Column(db.String(128))
    department = db.Column(db.String(128))
    institution = db.Column(db.String(128))

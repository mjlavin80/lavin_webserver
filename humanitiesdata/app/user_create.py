"""Create a new admin user able to view the /reports endpoint."""
from sqlalchemy import create_engine
import sys
from flask.ext.bcrypt import Bcrypt
from application import db, app
from application.models import User

#admin
password = 'b$lippity76@'
bcrypt = Bcrypt(app)
hashed = bcrypt.generate_password_hash(password)
ins = User(username='admin', is_admin=True, display_name='admin', email='lavin@pitt.edu', password=hashed, authenticated=True)

try:
    db.session.add(ins)
    db.session.commit()

except:
    db.session.rollback()

print "done."

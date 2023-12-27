from application import app, db
from application.models import *
import datetime

with app.app_context():
    db.drop_all()
    db.create_all()

print("DB created.")

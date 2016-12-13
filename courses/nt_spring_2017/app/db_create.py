from application import db
from application.models import *
import datetime

db.drop_all()
db.create_all()

print("DB created.")

from application import app, db
from application.models import *

with app.app_context():
    #PriceReviews.__table__.drop(db.session.bind)
    #PriceReviews.__table__.create(db.session.bind)
    GuidedResponse.__table__.create(db.session.bind)

print("DB altered.")

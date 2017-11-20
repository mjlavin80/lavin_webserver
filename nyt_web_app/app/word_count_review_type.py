import json
from application import *
from application.models import Metadata 

for i in range(1, 221):
    #instantiate a metadata query object
    rows = Metadata().query.filter(Metadata.word_count==str(i)).all()
    for r in rows:
        #use i values to set review_type
        r.review_type = "other"
        #commit
        db.session.commit()

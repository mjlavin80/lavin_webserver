import json
from application import *
from application.models import Metadata

rows = Metadata().query.all()
for h,i in enumerate(rows):
    int_version = int(i.word_count)
    i.review_word_count = int_version
    db.session.commit()
    if h % 100 == 0:
        print("done with %s" % h)

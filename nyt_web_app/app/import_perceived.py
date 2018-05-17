from sqlalchemy import create_engine
from application import *
from application.models import Metadata

import pandas as pd
all_rows = pd.read_csv("metadata.csv")

for i in all_rows.iterrows():
    as_listed = i[1][4]
    gender = i[1][5]
    nyt_id = i[1][3]
    row = Metadata().query.filter(Metadata.nyt_id == nyt_id).one_or_none()
    row.perceived_author_name = as_listed
    row.perceived_author_gender = gender
    try:
        db.session.add(row)
        db.session.commit()
    except:
        db.session.rollback()
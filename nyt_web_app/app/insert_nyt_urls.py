from sqlalchemy import create_engine
from application import *
from application.models import Metadata

import os
import glob
import json

data_dict = {}

for i in os.walk("/Users/matthewlavin/Desktop/1905"):
    a = glob.glob(i[0]+"/*.json")
    for u in a:
        with open(u) as meta:
            f = meta.read()
        data = json.loads(f)
        for row in data['response']['docs']:
            data_dict[row['_id']] = row['web_url']

metarows = Metadata.query.all()

for row in metarows:
	url = data_dict[row.nyt_id]
	row.nyt_pdf_endpoint = url
	try:
		db.session.commit()
	except:
		db.session.rollback()
from sqlalchemy import create_engine
from application import *
from application.models import Metadata
from application.insert_meta import insert_meta_from_json

import os, json
from collections import Counter

years = [str(i) for i in range(1906, 1926)]
#years = [str(i) for i in range(1857, 1930)]

for year in years:
    results = []    
    for z in range(1,13):
    

        month=str(z)
        
        #set paths
        base_path = "/Users/matthewlavin/nytimes/reviews"
        year_path = "".join([base_path, "/", year])
        new_path =  "".join([year_path, "/", month])

        with open(new_path+"/meta.json") as m:
            archive_meta = json.load(m)
            
            #loop all json files, open and read, find review content, add metadata to db
            for r in archive_meta['response']['docs']:
                rc = 0
                if r['type_of_material'] == 'Review':
                    rc = 1
                elif len(r['keywords']) > 0:
                    keywords= [i['value'].lower() for i in r['keywords']]
                     
                    if 'revs' in keywords:
                        rc += 1
                    if 'books and literature' in keywords:
                        rc +=1
                    if 'review' in keywords:
                        rc +=1
                    if 'reviews' in keywords:
                        rc +=1
                    if 'book review' in keywords:
                        rc +=1
                if rc > 0:
                    # check if already in db
                    meta = Metadata().query.filter(Metadata.nyt_id == r['_id']).one_or_none()
                    if meta:
                    	results.append("already_in_DB")
                    else:
                        # if not, add meta to db
                        result = insert_meta_from_json(r, month, year)
                        results.append(result)
        m.close()
    print(year, ": ", Counter(results).most_common())
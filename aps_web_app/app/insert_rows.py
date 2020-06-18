from sqlalchemy import create_engine
from application import *
from application.models import *
import pandas as pd
import sqlite3

skipped = []

mappings = {    
'ObjectType':'object_type',
'Contributor_OrganizationName':'organization_name', 
'LanguageCode':'language_code', 
'EISSN':'eissn', 
'Contributor_LastName':'last_name', 
'ActionCode':'action_code', 
'RecordID':'record_id', 
'StartPage':'start_page', 
'Contributor_MiddleName':'middle_name', 
'AlphaPubDate':'alpha_pub_date', 
'Contributor_PersonName':'person_name', 
'Publication_Title':'title', 
'Contributor_NameSuffix':'name_suffix', 
'ISSN':'issn', 
'Volume':'volume', 
'Publisher':'publisher', 
'DateTimeStamp':'date_time_stamp', 
'FullText':'full_text', 
'NumericPubDate':'numeric_pub_date', 
'Publication_Qualifier':'qualifier', 
'Version':'version', 
'Contributor_OriginalForm':'original_form', 
'Contributor_FirstName':'first_name', 
'Publication_PublicationID':'id', 
'Contributor_ContribRole':'role', 
'Abstract':'abstract', 
'RecordTitle':'record_title', 
'Issue':'issue', 
'Pagination':'pagination', 
'URLDocView':'url_doc_view', 
'Contributor_PersonTitle':'person_title', 
'SourceType':'source_type',
}

cols = list(mappings.keys())
cols.sort()

all_fields = [mappings[i] for i in cols]

reverse_lookup = dict(zip(all_fields, cols))

pub_fields = [i for i in cols if i.split("_")[0] == 'Publication']
contrib_fields = [i for i in cols if i.split("_")[0] == 'Contributor']
review_fields = [i for i in cols if i.split("_")[0] != 'Contributor' and i.split("_")[0] != 'Publication']

selectors = ", ".join(cols)
#print(len(cols), cols)

df = pd.read_csv('match_ids.csv')
ids = list(df['aps_id'])
formatter = ",".join(['?' for i in ids])

query = "".join(["SELECT", " ", selectors, " ", "FROM reviews WHERE RecordID IN (", formatter, ")"])  

conn = sqlite3.connect('aps_reviews_datastore.db')
c = conn.cursor()
rows = c.execute(query, ids).fetchall()

for e, u in enumerate(rows):
	if e > 50:
		break

	if e % 50 == 0:
		print(e)
	 
	lookup = dict(zip(cols, u))
	numeric_pub_date = lookup["NumericPubDate"]
	if int(numeric_pub_date) < 19260000 and int(numeric_pub_date) > 18800000:
		meta = Review().query.filter(Review.record_id == lookup['RecordID']).one_or_none()
		
		#insert review with foreign keys 
		if not meta:
			#id is foreign key
			pub_id = lookup["Publication_PublicationID"]
			pub = Publication.query.filter(Publication.id == pub_id).one_or_none()
			
			#insert pub if not exists
			if not pub:
				pub_cols = [mappings[i] for i in pub_fields]
				pub = Publication()
				for col in pub_cols:
					setattr(pub, col, lookup[reverse_lookup[col]])

				db.session.add(pub)
				db.session.commit()
			
			#insert contrib if not exists
			contrib_cols = [mappings[i] for i in contrib_fields]
			contrib_vals = [lookup[i] for i in contrib_fields]

			#make sure there are values
			data = False
			for i in contrib_vals:
				if len(i) > 0:
					data = True
					break
			if data:
				contrib = Contributor.query.filter(Contributor.original_form == lookup['Contributor_OriginalForm']).one_or_none()
				if not contrib:
					contrib = Contributor()
					for col in contrib_cols:
						setattr(contrib, col, lookup[reverse_lookup[col]])
					db.session.add(contrib)
					db.session.commit()
					contrib_id = contrib.id
			else:
				contrib_id = None
			
			#insert review with foreign keys 
			review_cols = [mappings[i] for i in review_fields]

			meta = Review()
			for col in review_cols:
				setattr(meta, col, lookup[reverse_lookup[col]])

			meta.pub_id = pub_id
			meta.contrib_id = contrib_id
			meta.status = "needs_audit"
			db.session.add(meta)
			db.session.commit()
		else:
			skipped.append(lookup['RecordID'])

print("skipped " + str(len(skipped)))
	
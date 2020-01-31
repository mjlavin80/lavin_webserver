from sqlalchemy import create_engine
from application import *
from application.models import *


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

import sqlite3

cols = list(mappings.keys())
cols.sort()

pub_fields = [i for i in cols if i.split("_")[0] == 'Publication']
contrib_fields = [i for i in cols if i.split("_")[0] == 'Contributor']
review_fields = [i for i in cols if i.split("_")[0] != 'Contributor' and i.split("_")[0] != 'Publication']

selectors = ", ".join(cols)
#print(len(cols), cols)

query = "".join(["SELECT", " ", selectors, " ", "FROM reviews ORDER BY random() LIMIT 495;"])
#print(query)

conn = sqlite3.connect('aps_reviews_datastore.db')
c = conn.cursor()
rows = c.execute(query).fetchall()
#print(rows[0])

#dconn = sqlite3.connect('datastore.db')
#dc = dconn.cursor()

for u in rows:
	#id is foreign key
	pub_id = lookup["Publication_PublicationID"]
	pub = Publication.query.filter(Publication.id == pub_id).one_or_none()
	if not pub:
		
	#meta = Review().query.filter(Review.record_id == aps_id).one_or_none()

	lookup = dict(zip(cols, u))
	#insert pub if not exists
	pub_cols = [mappings[i] for i in pub_fields]
	pub_vals = [lookup[i] for i in pub_fields]

	pub_query = "INSERT OR IGNORE INTO publication(" + ",".join(pub_cols) +") VALUES (?,?,?)"
	dc.execute(pub_query, pub_vals)
	dconn.commit()
	
	

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
		contrib_query = "INSERT OR IGNORE INTO contributor(id," + ",".join(contrib_cols) +") VALUES (null,?,?,?,?,?,?,?,?,?)"
		dc.execute(contrib_query, contrib_vals)
		dconn.commit()
		contrib_id = dc.lastrowid
	else:
		contrib_id = None
	#insert review with foreign keys 
	review_cols = [mappings[i] for i in review_fields]+["pub_id", "contrib_id", "status"]
	review_vals = [lookup[i] for i in review_fields]+[pub_id, contrib_id, "needs_audit"]

	review_query = "INSERT OR IGNORE INTO review(id," + ",".join(review_cols) +") VALUES (null,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
	dc.execute(review_query, review_vals)
	dconn.commit()

from application import *
from application.models import Metadata

def insert_meta_from_json(response, month, year):
    
    byline = response['byline']
    if byline == None:
        original = "na"
    else:
        original = byline['original']
    if original == None:
        original = "na"

    #instantiate a metadata object
    meta = Metadata()
    #use i values to set attrs
    meta.nyt_id = str(response['_id'])
    meta.month = str(month)
    meta.year = str(year)
    meta.document_type = str(response['document_type'])
    meta.headline = str(response['headline']['main'])
    meta.byline = str(original)
    meta.page = str(response['print_page'])
    meta.pub_date = str(response['pub_date'])
    meta.word_count = str(response['word_count'])
    meta.review_word_count = int(response['word_count'])
    meta.nyt_pdf_endpoint = response['web_url']

    #add default values for other things
    meta.corrected_transcription = "uncorrected"
    meta.review_type = "needs_audit"

    #add new data to session
    db.session.add(meta)

    #commit
    try:
        db.session.commit()
        return "success"
    except:
        db.session.rollback()
        return "failure"
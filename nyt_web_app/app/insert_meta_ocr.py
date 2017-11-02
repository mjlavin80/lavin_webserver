import json
from application import *
from application.models import Metadata

metadata_all = []
for i in range(1,13):
    month = str(i)
    metadata = "".join(["../nyt-reviews-poc/meta/", month, "/meta.json"])

    with open(metadata) as m:
        #print("Found metadata json for %s" % month)
        meta_json = m.read()
        archive_meta = json.loads(meta_json)
        for response in archive_meta['response']['docs']:
            byline = response['byline']
            if byline == None:
                original = "na"
            else:
                original = byline['original']
            if original == None:
                original = "na"
            if response['type_of_material']=="Review":
                metadata_all.append([response['_id'], month, "1905", response['document_type'], response['headline']['main'],
                                    original, response['print_page'], response['pub_date'], response['word_count']])

for i in metadata_all:
    #instantiate a metadata object
    meta = Metadata()
    #use i values to set attrs
    meta.nyt_id = str(i[0])
    meta.month = str(i[1])
    meta.year = str(i[2])
    meta.document_type = str(i[3])
    meta.headline = str(i[4])
    meta.byline = str(i[5])
    meta.page = str(i[6])
    meta.pub_date = str(i[7])
    meta.word_count = str(i[8])

    #insert ocr
    try:
        ocr_file_path = "".join(["../nyt-reviews-poc/ocr/nyt-", str(i[1]), "/", str(i[0]), ".txt"])
        with open(ocr_file_path) as o:
            ocr_raw = o.read()
            ocr_raw = ocr_raw.decode('utf-8')
        meta.ocr_transcription = ocr_raw
    except:
        meta.ocr_transcription = ""

    #add default values for other things
    meta.corrected_transcription = "uncorrected"
    meta.review_type = "unknown"

    #commit
    db.session.add(meta)
    db.session.commit()

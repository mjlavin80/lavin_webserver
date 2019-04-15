# import application files
from application import *
from application.models import Metadata, ClusterMeta

# get all from metadata where review_type = single_focus
# rows = Metadata().query.filter(Metadata.review_type == 'single_focus').all()

# # loop all get corrected transcription and nyt_id
# # write all transcriptions to ocr folder as txt files by id
# for row in rows:
# 	filename = ''.join(['ocr/', row.nyt_id, '.txt'])
# 	with open(filename, 'a') as f:
# 		f.write(row.corrected_transcription)
# 	f.close()

# get all from cluster where review_type = single_work
cluster_rows = ClusterMeta().query.filter(ClusterMeta.review_type == 'single_work').all()

#loop all and get transcription and nyt_id, with hyphen and cluster id
for cluster_row in cluster_rows:
	filename = ''.join(['ocr/', cluster_row.nyt_id, '-', str(cluster_row.id),'.txt'])
	with open(filename, 'a') as f:
		f.write(cluster_row.full_text)
	f.close()
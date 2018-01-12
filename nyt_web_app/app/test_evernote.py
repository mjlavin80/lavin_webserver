from evernote.api.client import EvernoteClient

client = EvernoteClient(
consumer_key = 'mjl4871',
consumer_secret = '5ab71a5ee7b1a92c',
sandbox=True # Default: True
)
request_token = client.get_request_token('http://localhost')
a = client.get_authorize_url(request_token)
print(request_token)

#http://localhost/?oauth_token=mjl4871.15FDFAA615F.687474703A2F2F6C6F63616C686F7374.FEF0F939EE1B240E2E2B713F9162DC1F&oauth_verifier=38226A2A10710ABD932A512966EB2FF7&sandbox_lnb=false
#oauth_token='mjl4871.15FDF813912.68747470733A2F2F6C6F63616C686F7374.6BD5C044D7AC49B8599B34AD9EB32075'
my_oauth_verifier='38226A2A10710ABD932A512966EB2FF7'
#'EDF77B25D0D9C3E25A8D47B1683940BD'

access_token = client.get_access_token(
oauth_token ='mjl4871.15FDFAA615F.687474703A2F2F6C6F63616C686F7374.FEF0F939EE1B240E2E2B713F9162DC1F',
oauth_token_secret = request_token['oauth_token_secret'],
oauth_verifier = my_oauth_verifier
)

client = EvernoteClient(token=access_token)
note_store = client.get_note_store()
notebooks = note_store.listNotebooks()
print(notebooks)

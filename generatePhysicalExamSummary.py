import requests
import os
from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import download_object, upload_json, download_json
from dotenv import load_dotenv
from google.cloud import storage

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

# port = 9999
# conn = PyCPN()
# conn.accept(port)
# load_dotenv()
# storage_client = storage.Client()

# creds, project = google.auth.default()
# auth_req = google.auth.transport.requests.Request()
# creds.refresh(auth_req)
# Now you can use creds.token

def get_text(object_uri):
	file_name = "recognition_text"
	download_object(storage_client, file_name, object_uri)
	with open(f"resources/{file_name}") as f:
		contents = f.read()
		return contents
# Instantiate a Google Cloud Storage client and specify required bucket and file
storage_client = storage.Client()
bucket = storage_client.get_bucket('bucket_name')
blob = bucket.blob('filename.json')

# Download the contents of the blob as a string and then parse it using json.loads() method
data = json.loads(blob.download_as_string(client=None))
# import google.auth
# import google.auth.transport.requests
def get_json(objectUri):
	return download_json(storage_client, objectUri)

def get_object_entity_mentions(objectUris=["",""]):
	out = []
	for uri in objectUris:
		data = download_json(storage_client,uri)
		aggregatedData = {
			entityMentions: [mention for mention in data["entityMentions"]],
			entities: [mention for mention in data["entities"]]
		}
		out.append(mentions)
	return out

if __name__ == "__main__":
   print(get_object_entity_mentions([
	"gs://vpe-text-recognition/290c634358424c51bf53229514d68839.json",
	"gs://vpe-text-recognition/89f1833e3eaa451c8c33b365d961ee5a.json"]))


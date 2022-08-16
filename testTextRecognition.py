import requests
from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import download_object, upload_json
from dotenv import load_dotenv
from google.cloud import storage
import google.auth
import google.auth.transport.requests

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example
storage_client = storage.Client()

creds, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-healthcare"])
auth_req = google.auth.transport.requests.Request()
creds.refresh(auth_req)

def get_text(object_uri):
	file_name = "recognition_text"
	download_object(storage_client, file_name, object_uri)
	with open(f"resources/{file_name}") as f:
		contents = f.read()
		return contents

def upload_text_recognition(object_uri):
	baseUrl = "https://healthcare.googleapis.com/v1"
	project = "virtual-physical-examination"
	location = "us-central1"
	service = "nlp:analyzeEntities"
	url = baseUrl + f"/projects/{project}/locations/{location}/services/{service}"
	
	bearerToken = creds.token
	headers = { "Authorization": f"Bearer {bearerToken}", "Content-Type": "application/json" }
	
	nlpService = "projects/virtual-physical-examination/locations/us-central1/services/nlp"
	documentContent = get_text(object_uri)
	licensedVocabularies = ['SNOMEDCT_US','ICD10CM']
	json = { "nlpService": nlpService, "documentContent": documentContent, "licensedVocabularies": licensedVocabularies }
	
	response_json = requests.post(url, headers=headers, json=json).json()
	text_recognition_uri = upload_json(storage_client, "vpe-text-recognition", response_json)
	print(f"Finished text recognition of object uri: {object_uri}.")
	return text_recognition_uri

def doit():
	port = 9999
	conn = PyCPN()
	conn.accept(port)
	load_dotenv()
	while True:
		objectUri = stringDecode(conn.receive())
		if objectUri == 'quit':
			conn.disconnect()
			break
		else:
			textRecognitionUri = upload_text_recognition(objectUri)
			conn.send(stringEncode(textRecognitionUri))

if __name__ == "__main__":
    doit()
	


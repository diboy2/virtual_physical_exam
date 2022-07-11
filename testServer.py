import requests
import os
from pyCPN import PyCPN
from pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

port = 9999
conn = PyCPN()
conn.accept(port)
load_dotenv()
def doit():
	while True:
		physicianLog = stringDecode(conn.receive())
		if physicianLog == 'quit':
			conn.disconnect()
			break
		else:
			print("This is my physician log: " + physicianLog)
			
			baseUrl = "https://healthcare.googleapis.com/v1"
			project = "virtual-physical-examination"
			location = "us-central1"
			service = "nlp:analyzeEntities"
			url = baseUrl + f"/projects/{project}/locations/{location}/services/{service}"
			
			bearerToken = os.getenv('BEARER_TOKEN')
			headers = { "Authorization": f"Bearer {bearerToken}", "Content-Type": "application/json" }
			
			nlpService = "projects/virtual-physical-examination/locations/us-central1/services/nlp"
			documentContent = physicianLog
			licensedVocabularies = ['SNOMEDCT_US','ICD10CM']
			json = { "nlpService": nlpService, "documentContent": documentContent, "licensedVocabularies": licensedVocabularies }
			
			response = requests.post(url, headers=headers, json=json)
			print(response.json())
			conn.send(stringEncode(str(physicianLog)))
			break

if __name__ == "__main__":
   doit()


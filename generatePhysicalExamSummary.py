import requests
import os
from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import upload_html, download_json
from dotenv import load_dotenv
from google.cloud import storage
from json2html import *

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

# port = 9996
# conn = PyCPN()
# conn.accept(port)
# load_dotenv()
# storage_client = storage.Client()

# Instantiate a Google Cloud Storage client and specify required bucket and file
storage_client = storage.Client()

def upload_exam_summary(htmlSummary):
	return upload_html(storage_client, "vpe-exam-summary", htmlSummary)

def get_object_entity_mentions(objectUris=["",""]):
	out = ""
	for uri in objectUris:
		data = download_json(storage_client,uri)
		out += json2html.convert(json = data)
	return out

def process_uri_list(uriList):
	htmlSummary = get_object_entity_mentions(uriList.split(","))
	return upload_exam_summary(htmlSummary)

def doit():
	while True:
		objectUriList = stringDecode(conn.receive())
		if objectUriList == 'quit':
			conn.disconnect()
			break
		else:
			summaryUri = process_uri_list(objectUriList)
			conn.send(stringEncode(summaryUri))

if __name__ == "__main__":
	tup = ["gs://vpe-text-recognition/baa491cddb4948b68c6735fd438f4de7.json","gs://vpe-text-recognition/5c4cd61592a0490cbb33df57c6447192.json","gs://vpe-text-recognition/94778f202c9d415e83693ff805f12544.json","gs://vpe-text-recognition/0d131dd3ae5f4d3b8ad514534d0344ee.json","gs://vpe-text-recognition/e85164e6fd8c45d5b21b889283cb60ba.json","gs://vpe-text-recognition/cfc4cf95c3fc480b9e947f204d888aef.json","gs://vpe-text-recognition/448ce878de7c4c95a9ef95d273f11ad1.json","gs://vpe-text-recognition/431d79c89aa34bf69add94de63b7c9b7.json","gs://vpe-text-recognition/d3b34876168c407fb0ad62b12a444a96.json","gs://vpe-text-recognition/53f26ebdcd6f45749b472a73b9d9f9cc.json","gs://vpe-text-recognition/52d9a6e66326440e86ca216edfa69cb4.json","gs://vpe-text-recognition/293cf5d017344721b6ddbc6543a6cd88.json","gs://vpe-text-recognition/923ae163d68b4c16bd0835f3dfbc11fe.json","gs://vpe-text-recognition/dd5f40610b0f4e988a0abccbf51a33ce.json"]
	process_uri_list(",".join(tup))


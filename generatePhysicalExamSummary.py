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

port = 9996
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

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
	doit()


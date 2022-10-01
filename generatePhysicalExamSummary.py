from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import upload_html, download_json
from dotenv import load_dotenv
from google.cloud import storage
from json2html import *

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1

port = 9996
conn = PyCPN()
conn.accept(port)
load_dotenv()

# Instantiate a Google Cloud Storage client and specify required bucket and file
storage_client = storage.Client()

def upload_exam_summary(htmlSummary):
	return upload_html(storage_client, "vpe-exam-summary", htmlSummary)

def get_object_entity_mentions(objectUris):
	out = ""
	def map_entity_mentions(entity_mention):
		return dict({
			"type": entity_mention["type"],
			"textContent": entity_mention["text"]["content"],
			"confidence": entity_mention["confidence"]
		})
	def map_entities(entity):
		return dict ({
			"preferredTerm": entity["preferredTerm"],
			"vocabularyCodes": entity["vocabularyCodes"][0]
		})
	
	table_data = table_data = dict({
		"entityMentions": [],
		"entities": []
	})
	for uri in objectUris:
		data = download_json(storage_client,uri)	
		table_data["entityMentions"] += list(map(map_entity_mentions,data["entityMentions"]))
		table_data["entities"] += list(map(map_entities, data["entities"]))
	
	return json2html.convert(json = table_data["entityMentions"]) + "<br/>" +  json2html.convert(json = table_data["entities"]) 

def process_uri_list(uriList = "gs://vpe-text-recognition/fd65ff44541c44d6ae8afbcec8af313f.json,gs://vpe-text-recognition/c985aac5da024959888c56fa7c8e969d.json"):
	print(uriList)
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
	process_uri_list()


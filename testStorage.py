from pyCPN import PyCPN
from pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage

import uuid
# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

port = 9000
conn = PyCPN()
conn.accept(port)
load_dotenv()

def upload_text(bucket_name, metrics):
	storage_client = storage.Client()
	bucket = storage_client.bucket(bucket_name)
	object_name = str(uuid.uuid4().hex)
	blob = bucket.blob(object_name)
	blob.upload_from_string(metrics)

	print(f"{object_name} with metrics {metrics} uploaded to {bucket_name}.")
	return object_name

def doit():
	while True:
		metrics = stringDecode(conn.receive())
		if metrics == 'quit':
			conn.disconnect()
			break
		else:
			object_name = upload_text("vpe-daily-metrics", metrics)
			conn.send(stringEncode(object_name))
			break

if __name__ == "__main__":
   doit()


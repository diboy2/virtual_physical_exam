from pyCPN import PyCPN
from pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage
import uuid

port = 9000
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

def download_object(file_name, uri):	
	with open(f"resources/{file_name}", 'wb') as file_obj:
		storage_client.download_blob_to_file(uri, file_obj)

def upload_text(bucket_name, medical_history):
	bucket = storage_client.bucket(bucket_name)
	object_name = str(uuid.uuid4().hex)
	blob = bucket.blob(object_name)
	blob.upload_from_string(medical_history)

	print(f"{object_name} with medical history {medical_history} uploaded to {bucket_name}.")
	return f"gs://{bucket_name}/{object_name}"

def doit():
	while True:
		medical_history = stringDecode(conn.receive())
		if medical_history == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_text("vpe-medical-history", medical_history)
			conn.send(stringEncode(url))
			break

if __name__ == "__main__":
	doit()

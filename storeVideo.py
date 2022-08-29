from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage
import uuid

port = 9002
conn = PyCPN()
conn.accept(port)
load_dotenv()

storage_client = storage.Client()

def download_object(file_name, uri):	
	with open(f"resources/{file_name}", 'wb') as file_obj:
		storage_client.download_blob_to_file(uri, file_obj)


def upload_file(bucket_name, file_name):
	bucket = storage_client.bucket(bucket_name)
	object_name = str(uuid.uuid4().hex)
	blob = bucket.blob(object_name)
	blob.upload_from_filename(file_name)

	print(f"{object_name} with file name {file_name} uploaded to {bucket_name}.")
	return f"gs://{bucket_name}/{object_name}"

def doit():
	while True:
		file = stringDecode(conn.receive())
		if file == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_file("vpe-video", f"resources/{file}.mp4")
			conn.send(stringEncode(url))
			break

if __name__ == "__main__":
	doit()

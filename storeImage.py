from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage
import uuid

port = 9001
conn = PyCPN()
conn.accept(port)
load_dotenv()

storage_client = storage.Client()


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
			url = upload_file("vpe-images", f"resources/{file}.jpg")
			conn.send(stringEncode(url))
			break

if __name__ == "__main__":
	doit()

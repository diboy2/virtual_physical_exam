import uuid
import json
from google.cloud.storage.blob import Blob

def download_object(storage_client, file_name, uri):	
	with open(f"resources/{file_name}", 'wb') as file_obj:
		storage_client.download_blob_to_file(uri, file_obj)

def download_json(storage_client, uri):
	blob = Blob.from_string(uri, client=storage_client)
	jsonString = blob.download_as_string()
	return json.loads(jsonString)

def upload_text(storage_client, bucket_name, text):
	bucket = storage_client.bucket(bucket_name)
	object_name = str(uuid.uuid4().hex)
	blob = bucket.blob(object_name)
	blob.upload_from_string(text)

	print(f"{object_name} with text {text} uploaded to {bucket_name}.")
	return f"gs://{bucket_name}/{object_name}"

def upload_json(storage_client, bucket_name, data):
	bucket = storage_client.bucket(bucket_name)
	object_name = f"{str(uuid.uuid4().hex)}.json"
	blob = bucket.blob(object_name)
	blob.upload_from_string(
        data=json.dumps(data),
        content_type='application/json'
    )
	print(f"{object_name} with json uploaded to {bucket_name}.")
	return f"gs://{bucket_name}/{object_name}"


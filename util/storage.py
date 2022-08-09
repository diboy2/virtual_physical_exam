import uuid

def download_object(storage_client, file_name, uri):	
	with open(f"resources/{file_name}", 'wb') as file_obj:
		storage_client.download_blob_to_file(uri, file_obj)

def upload_text(storage_client, bucket_name, text):
	bucket = storage_client.bucket(bucket_name)
	object_name = str(uuid.uuid4().hex)
	blob = bucket.blob(object_name)
	blob.upload_from_string(text)

	print(f"{object_name} with text {text} uploaded to {bucket_name}.")
	return f"gs://{bucket_name}/{object_name}"
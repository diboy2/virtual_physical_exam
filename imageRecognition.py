from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage, vision
from util.storage import upload_text

load_dotenv()
storage_client = storage.Client()

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

port = 9998
conn = PyCPN()
conn.accept(port)

def get_joined_labels(imageUri = "gs://vpe-images/64e567ec584f430ebb892c77e18e9394"):
	client = vision.ImageAnnotatorClient()

	# The name of the image file to annotate
	response = client.label_detection({
		'source': { 'image_uri': imageUri }
	})
	print(f"Finished image recognition of image uri: {imageUri}.")

	descriptions = list(map(lambda label: label.description, response.label_annotations))
	return ' '.join(descriptions)

def doit():
	while True:
		imageUri = stringDecode(conn.receive())
		if imageUri == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_text(storage_client, "vpe-image-recognition", get_joined_labels(imageUri))
			conn.send(stringEncode(url))

if __name__ == "__main__":
	doit()
	# url = upload_text(storage_client, "vpe-image-recognition", get_joined_labels())
	# print(url)
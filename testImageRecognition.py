import io
from pyCPN import PyCPN
from pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import vision

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

port = 9998
conn = PyCPN()
conn.accept(port)
load_dotenv()

def get_joined_labels(imageUri):
	client = vision.ImageAnnotatorClient()
	
	# The name of the image file to annotate
	response = client.label_detection({
		'source': { 'image_uri': imageUri }
	})

	descriptions = list(map(lambda label: label.description, response.label_annotations))
	return ' '.join(descriptions)
	
def doit():
	while True:	
		imageUri = stringDecode(conn.receive())
		if imageUri == 'quit':
			conn.disconnect()
			break
		else:
			conn.send(stringEncode(get_joined_labels(imageUri)))
			break

if __name__ == "__main__":
	doit()

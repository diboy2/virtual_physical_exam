import io
import os
from pyCPN import PyCPN
from pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import vision

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

# port = 9998
# conn = PyCPN()
# conn.accept(port)
# load_dotenv()

def recognize_image():
	# Instantiates a client
	client = vision.ImageAnnotatorClient()
	
	# The name of the image file to annotate
	file_name = os.path.abspath('resources/testImage.jpg')

	# Loads the image into memory
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()

	image = vision.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations
	
	print('Labels:')
	for label in labels:
		print(label.description)

def doit():
	while True:
		physicianLog = stringDecode(conn.receive())
		if physicianLog == 'quit':
			conn.disconnect()
			break
		else:
			recognize_image()
			break

if __name__ == "__main__":
   recognize_image()

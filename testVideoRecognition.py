from pyCPN import PyCPN
from util.pyEncodeDecode import stringEncode, stringDecode
from dotenv import load_dotenv
from google.cloud import storage, videointelligence
from util.storage import upload_text

# Tested with Python v 3.7.2 and CPN Tools v 4.0.1
# Server for use with processWeatherClient.cpn model example

port = 9997
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

def get_joined_labels(videoUri):
	client = videointelligence.VideoIntelligenceServiceClient()
	features = [videointelligence.Feature.LABEL_DETECTION]

	# The name of the video file to annotate
	response = client.annotate_video(
		request= { "features": features, 'input_uri': videoUri }
	)

	result = response.result(timeout=90)
	print(f"Finished video recognition of video uri: {videoUri}.")

	segment_labels = result.annotation_results[0].segment_label_annotations
	labels = []

	for i, segment_label in enumerate(segment_labels):
		categories = map(lambda category: category.description,segment_label.category_entities )
		labels.append({ "label": segment_label.entity.description, "categories": categories})

	return ' '.join(labels)

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
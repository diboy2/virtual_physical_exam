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

	# The name of the image file to annotate
	response = client.annotate_video(
		request= { "features": features, 'input_uri': videoUri }
	)
	print(f"Finished video recognition of video uri: {videoUri}.")

	result = response.result(timeout=90)
	print("\nFinished processing.")
	# Process video/segment level label annotations
	segment_labels = result.annotation_results[0].segment_label_annotations
	for i, segment_label in enumerate(segment_labels):
		print("Video label description: {}".format(segment_label.entity.description))
		for category_entity in segment_label.category_entities:
			print(
				"\tLabel category description: {}".format(category_entity.description)
			)

		for i, segment in enumerate(segment_label.segments):
			start_time = (
				segment.segment.start_time_offset.seconds
				+ segment.segment.start_time_offset.microseconds / 1e6
			)
			end_time = (
				segment.segment.end_time_offset.seconds
				+ segment.segment.end_time_offset.microseconds / 1e6
			)
			positions = "{}s to {}s".format(start_time, end_time)
			confidence = segment.confidence
			print("\tSegment {}: {}".format(i, positions))
			print("\tConfidence: {}".format(confidence))
		print("\n")
	descriptions = list(map(lambda label: label.description, response.label_annotations))
	return ' '.join(descriptions)
"""Detect labels given a file path."""
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.Feature.LABEL_DETECTION]

with io.open(path, "rb") as movie:
    input_content = movie.read()

operation = video_client.annotate_video(
    request={"features": features, "input_content": input_content}
)
print("\nProcessing video for label annotations:")

result = operation.result(timeout=90)
print("\nFinished processing.")

# Process video/segment level label annotations
segment_labels = result.annotation_results[0].segment_label_annotations
for i, segment_label in enumerate(segment_labels):
    print("Video label description: {}".format(segment_label.entity.description))
    for category_entity in segment_label.category_entities:
        print(
            "\tLabel category description: {}".format(category_entity.description)
        )

    for i, segment in enumerate(segment_label.segments):
        start_time = (
            segment.segment.start_time_offset.seconds
            + segment.segment.start_time_offset.microseconds / 1e6
        )
        end_time = (
            segment.segment.end_time_offset.seconds
            + segment.segment.end_time_offset.microseconds / 1e6
        )
        positions = "{}s to {}s".format(start_time, end_time)
        confidence = segment.confidence
        print("\tSegment {}: {}".format(i, positions))
        print("\tConfidence: {}".format(confidence))
    print("\n")


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
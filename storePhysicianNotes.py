from dotenv import load_dotenv
from google.cloud import storage
from util.pyCPN import PyCPN 
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import upload_text

port = 9004
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

def doit():
	while True:
		physician_notes = stringDecode(conn.receive())
		if physician_notes == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_text(storage_client, "vpe-physician-notes", physician_notes)
			conn.send(stringEncode(url))

if __name__ == "__main__":
	doit()

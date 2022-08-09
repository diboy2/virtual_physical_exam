from dotenv import load_dotenv
from google.cloud import storage
from util.pyCPN import PyCPN 
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import upload_text

port = 9000
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

def doit():
	while True:
		medical_history = stringDecode(conn.receive())
		if medical_history == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_text(storage_client,"vpe-medical-history", medical_history)
			conn.send(stringEncode(url))
			break

if __name__ == "__main__":
	doit()

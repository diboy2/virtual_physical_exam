from dotenv import load_dotenv
from google.cloud import storage
from util.pyCPN import PyCPN 
from util.pyEncodeDecode import stringEncode, stringDecode
from util.storage import upload_text

port = 9002
conn = PyCPN()
conn.accept(port)
load_dotenv()
storage_client = storage.Client()

def doit():
	while True:
		metrics = stringDecode(conn.receive())
		if metrics == 'quit':
			conn.disconnect()
			break
		else:
			url = upload_text(storage_client,"vpe-daily-metrics", metrics)
			conn.send(stringEncode(url))
			break

if __name__ == "__main__":
	doit()

import json
import socket
import time

msgHeader = "[VISION]: "

TRACKER_HOST = "tracker.local"
TRACKER_PORT = 1520

BUF_SIZE = 1024

TRACK_PHRASE = "track".encode('utf-8')
CAPTURE_MAP_PHRASE = "capture_map".encode('utf-8')

class Vision():
	def __init__(self):
		self.client = Client()
		print(msgHeader + "Connecting to the tracker...")
		# Try to connect to the tracker server.
		if not self.client.connect():
			print(msgHeader + "Could not connect to the tracker. Exiting...")
			exit()
		print(msgHeader + "Initialisation complete.")

	def get_tracker_data(self):
		data = parse_json(self.client.send_message(TRACK_PHRASE))
		return data

	def get_capture_map_data(self):
		print(msgHeader + "Requesting waypoint capture from tracker...")
		data = parse_json(self.client.send_message(CAPTURE_MAP_PHRASE))
		if data is not None and "waypoints" in data:
			print(msgHeader + "Recieved " + str(len(data["waypoints"])) + " waypoint(s) from tracker.")
			print(data)
			return data["waypoints"]
		else:
			print(msgHeader + "No waypoints recieved from tracker.")
			return []


	# Return the ID, pixel coordinates and orientation of every ZenWheels car.
	def locateCars(self):
		visionData = self.get_tracker_data()
		if visionData == None:
			return []
		return visionData


# TODO: Make server interactions non-blocking?
class Client:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.isConnected = False

	def connect(self):
		try:
			self.s.settimeout(3)  # Timeout after a 3 second wait.
			self.s.connect((socket.gethostbyname(TRACKER_HOST), TRACKER_PORT))
			self.s.settimeout(None)  # Set socket back to blocking.
			self.isConnected = True
			return True
		except Exception as e:
			print(e)
			return False

	def send_message(self, msg):
		try:
			self.s.send(msg)
			data = self.s.recv(BUF_SIZE)
			return data
		except Exception as e:
			print("LASTMSG: ", msg)
			print(e)
			self.isConnected = False
			print(msgHeader + "Lost connection to tracker.")



def parse_json(msg):
	if msg is None or msg == b'':
		return None
	try:
		dict = json.loads(msg.decode('utf-8'))
		return dict
	except Exception as e:
		print("BAD MSG: ", msg)
		print("JSON:", e)
		return None


if __name__ == "__main__":
	v = Vision()

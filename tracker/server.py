import json
import socketserver
import threading
import capture_map

TRACKER_HOST = "0.0.0.0"
TRACKER_PORT = 1520

BUF_SIZE = 1024


class Server():
	isConnected = False
	latest_data = None
	calibration = None
	car_identification = None

	def __init__(self):
		self.server = ThreadedTCPServer((TRACKER_HOST, TRACKER_PORT), ThreadedTCPRequestHandler)
		server_thread = threading.Thread(target=self.server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
		print("Server loop running in thread:", server_thread.name)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
	def handle(self):
		# self.request.settimeout(1) # Why is this here again?
		Server.isConnected = True
		print("Received connection from " + str(self.client_address[0]) + ".")
		while True:
			try:
				data = self.request.recv(BUF_SIZE)
				message = data.decode('utf-8')
				print("[TRACKER]: Message Recieved: " + message)
				if message == "track":
					response = encode_json(Server.latest_data)
				elif message == "calibrate":
					response = encode_json(Server.calibration)
				elif message == "identify":
					response = encode_json(Server.car_identification)
				elif message == "capture_map":
					response = encode_json(capture_map.get_response())
				else:
					response = "[TRACKER]: No arguments detected."
				self.request.sendall(response.encode('utf-8'))
			except:
				Server.isConnected = False
				print("Client " + str(self.client_address[0]) + " disconnected.")
				break


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	pass


def encode_json(dict):
	try:
		msg = json.dumps(dict)
		return msg
	except Exception as e:
		print("BAD MSG: ", dict)
		print("JSON: ", e)
		return None

import socket
import sys
import traceback
from threading import Thread

def startServer():
	host = ""
	port = 12345	 # arbitrary non-privileged port

	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
	print("Socket created")

	connections = []

	try:
		soc.bind((host, port))
	except:
		print("Bind failed. Error : " + str(sys.exc_info()))
		sys.exit()

	soc.listen(8)	   # queue up to 5 requests
	print("Socket now listening")

	numPlayers = 2
	numConnections = 0
	while numConnections < numPlayers:
		connection, address = soc.accept()
		connections.append(connection)

		ip, port = str(address[0]), str(address[1])
		print("Connected with " + ip + ":" + port)

		try:
			Thread(target=clientThread, args=(connection, ip, port)).start()
			numConnections += 1
		except:
			print("Thread did not start.")
			traceback.print_exc()

	soc.close()
	print("serverSocketClosed, can start boardgame!")
	return connections


def clientThread(connection, ip, port, max_buffer_size = 5120):
	isActive = True
	# Welcome player
	sendMessageToClient(connection, "Welcome!", 5280)
	print(receiveInput(connection, 5280))
	while isActive:
		client_input = receiveInput(connection, max_buffer_size)

		if "--QUIT--" in client_input:
			print("Client is requesting to quit")
			connection.close()
			print("Connection " + ip + ":" + port + " closed")
			isActive = False
		else:
			print("Processed result: {}".format(client_input))
			connection.sendall("-".encode("utf8"))


def sendMessageToClient(connection, message, max_buffer_size, expectResponse=False):
	 connection.sendall(message.encode("utf8"))
	 connection.sendall(str(expectResponse).encode("utf8"))

def receiveInput(connection, max_buffer_size):
	client_input = connection.recv(max_buffer_size)
	client_input_size = sys.getsizeof(client_input)

	if client_input_size > max_buffer_size:
		print("The input size is greater than expected {}".format(client_input_size))

	decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
	result = process_input(decoded_input)

	return result


def process_input(input_str):
	print("Processing the input received from client")

	return "Hello " + str(input_str).upper()

startServer()

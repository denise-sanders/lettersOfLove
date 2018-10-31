
# Import socket module 
import socket                
  
s = socket.socket()          
  
port = 12345                
  
def sendMessageToServer():
	message = input()
	s.sendall(message.encode("utf8"))

# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 
while True:
	messageFromServer = s.recv(1024) 
	try:
		messageFromServer = messageFromServer.decode("utf8")
		if messageFromServer == str(True):
			sendMessageToServer()
	except Exception as e:
		print(str(e))
		print(messageFromServer)

s.close()     


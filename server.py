
import socket                
  

s = socket.socket()          
print "Socket successfully created"
  
port = 12345                
s.bind(('', port))         
print "socket binded to %s" %(port) 
  
s.listen(5)      
print "socket is listening"            
  
# a forever loop until we interrupt it or  
# an error occurs 
while True: 
  
   # Establish connection with client. 
   c, addr = s.accept()      
   print 'Got connection from', addr 
  
   c.send('Thank you for connecting') 
  
   c.close()
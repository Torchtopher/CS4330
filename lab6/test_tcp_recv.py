import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

serversocket.bind(('0.0.0.0', 8082)) 
serversocket.listen(10)

running = True
while running: 
   connection, address = serversocket.accept() 
   buf = connection.recv(512).decode()
   print("Received:", buf)

serversocket.close()


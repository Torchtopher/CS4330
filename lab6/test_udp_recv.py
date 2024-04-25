import socket

B_IP = "255.255.255.255"
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 8082)) # Required on Windows

while True:
    data, addr = client.recvfrom(1024) # Server get 1024 bytes
    print("Received:", data.decode() + " from " + str(addr))

client.close()

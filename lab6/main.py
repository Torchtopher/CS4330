import socket
import redis
import time
import argparse
import ipaddress
from subprocess import check_output
import threading

NUM = None
ips = check_output(['hostname', '--all-ip-addresses'])
OUR_IP = ips.decode().split(' ')[0]
REDIS_KEY = "connections"

print('OUR_IP:', OUR_IP)

# stolen from https://stackoverflow.com/questions/3462784/check-if-a-string-matches-an-ip-address-pattern-in-python
def is_ipv4(string):
    try:
        ipaddress.IPv4Network(string)
        return True
    except ValueError:
        return False

def broadcast_thread():
    global NUM
    import socket

    B_IP = "255.255.255.255"
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client.bind(("", 8082)) # not on windows but won't hurt

    while True:
        #print("\nBroadcasting...")
        data = f"Hello, I am {OUR_IP} and my number is {NUM}"
        client.sendto(data.encode(), (B_IP, 8082))
        time.sleep(5)

def tcp_recv():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_client:
        tcp_client.bind(('0.0.0.0', 8082)) 
        tcp_client.listen(10)
        while True: 
            # not sure if we will recive more than 1 message from this connection, I don't think it works in that case as it only stores the last message
            connection, address = tcp_client.accept() 
            data = connection.recv(1024).decode()
            # data looks like "Hello, I am <IP> and my number is <NUM>"
            recved_num = int(data.split()[-1])
            print(f"\nTCP RECVD: {address[0]} {recved_num}")

    
def udp_recv():
    global redis_server
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) as udp_client:
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udp_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp_client.bind(("", 8082)) # Required on Windows
        while True:
            data, addr = udp_client.recvfrom(1024) # up to 1024 bytes
            # data looks like "Hello, I am <IP> and my number is <NUM>"
            recved_num = int(data.decode().split()[-1])
            print(f"\nUDP RECVD: {addr[0]} {recved_num}")
            tcp_send(addr[0])
            # no point in storing same address multiple times 
            if addr[0] not in redis_server.lrange(REDIS_KEY, 0, -1):
                redis_server.lpush(REDIS_KEY, addr[0])


def tcp_send(address):
    print('Connecting over TCP to', address)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((address, 8082)) 

    running = True 
    data = f"Hello, I am {OUR_IP} and my number is {NUM}"
    client_socket.send(data.encode())
    client_socket.close()        

def main():
    global NUM
    parser = argparse.ArgumentParser(description='P2P Server for lab 6')
    parser.add_argument('NUM', type=int, help='Positive integer that others will recive from this server')
    parser.add_argument('-b', action='store_true', help='Enable Broadcast mode')
    args = parser.parse_args()
    if args.NUM < 0:
        print('NUM should be positive - exiting...')
        return
    NUM = args.NUM
    print('NUM:', NUM)
    # start tcp and udp recivers
    t1 = threading.Thread(target=tcp_recv)
    t1.daemon = True # so that it will exit when main thread exits
    t1.start()
    t2 = threading.Thread(target=udp_recv)
    t2.daemon = True
    t2.start()

    if args.b:
        print('Broadcast mode enabled')
        # start broadcast thread
        t = threading.Thread(target=broadcast_thread)
        t.daemon = True
        t.start()
    else:
        print('Broadcast mode disabled')

    while True:
        try:
            ADDRESS = input("Enter the adress of server to connect (or exit): ")
        except KeyboardInterrupt:
            print('\nCTRL-C, Exiting...')
            break
        if ADDRESS.lower() == 'exit':
            print('Exiting...')
            break
        elif ADDRESS.lower() == 'conns':
            for i in range(0, redis_server.llen(REDIS_KEY)):
                print(redis_server.lindex(REDIS_KEY, i))
            continue
        elif ADDRESS == "":
            continue
        elif not is_ipv4(ADDRESS):
            print('Invalid IP address, try again')
            continue

        tcp_send(ADDRESS) # send message to IP address entered

if __name__ == '__main__':
    global redis_server 
    redis_server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_server.delete(REDIS_KEY) # remove old connections 
    main()
import socket
import time
import random

HOST = "255.255.255.255"
PORT = 28010
new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
addr = None

try:
    while True:
        new_sock.sendto(b"Who is Chat-CLI server? 1.0.0", (HOST, PORT))
        packet = new_sock.recvfrom(4096)
        
        r = random.randrange(0, 10) / 10
        print(r)
        time.sleep(random.randrange(0, 8) / 10)

        addr = packet[1]

        if packet[0] == b"":
            break
        
        if packet[0] == b'I am Chat-CLI server. 1.0.0':
            new_sock.sendto(b"Chat-CLI Client Acknowledge. 1.0.0", (HOST, PORT))                
        
except KeyboardInterrupt:
    pass


new_sock.close()
print("Connection establish from", addr)

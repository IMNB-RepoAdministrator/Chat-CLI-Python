import socket

HOST = socket.gethostbyname(socket.gethostname())
BROADCAST = "255.255.255.255"
PORT = 20000
server = []

broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

message = b'LAN: Request connect.'
broadcast.sendto(message, (BROADCAST, PORT))

packet = broadcast.recvfrom(4096)

message_server = packet[0]
addr = packet[1]

if message_server == b'LAN: Request connect.':
    server.append(addr)
    print(server)
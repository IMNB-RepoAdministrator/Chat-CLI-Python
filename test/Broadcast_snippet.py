import socket

HOST = socket.gethostbyname(socket.gethostname())
BROADCAST = "0.0.0.0"
PORT = 20000

broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast.bind((BROADCAST, PORT))
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
accepted_address = []

while True:
    message = b''
    
    while message == b'':
        packet = broadcast.recvfrom(4096)
        message = packet[0]
        addr = packet[1]
        
        print(message, addr)
        
        if message != b'LAN: Request connect.':
            message = b''
            
        else:
            accepted_address.append(addr)
            broadcast.sendto(message, addr)
            break
    
    print(accepted_address)
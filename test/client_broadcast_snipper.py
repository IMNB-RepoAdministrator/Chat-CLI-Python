import random
import socket
import time

# Create UDP socket and save broadcast address and port.
HOST = "255.255.255.255"
PORT = 28010
new_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
new_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
addr = None

try:
    while True: # Connection loop (Discover).
        new_sock.sendto(b"Who is Chat-CLI server? 1.0.0", (HOST, PORT))  # Send request
        
        # This in actual `client_broadcast should have timeout duration instead of waiting indefinitely
        packet = new_sock.recvfrom(4096)
        
        # This is just to emulate inconsistant connection.
        r = random.randrange(0, 10) / 10
        print(r)
        time.sleep(random.randrange(0, 8) / 10)

        # Get address from packet got from server
        addr = packet[1]

        # Check if packet data content is valid with the protocol.
        if packet[0] == b"":
            break
        
        if packet[0] == b'I am Chat-CLI server. 1.0.0': # 1.0.0 should be replace with `version` in sharedconfig.yaml
            new_sock.sendto(b"Chat-CLI Client Acknowledge. 1.0.0", (HOST, PORT)) # same like above
        
except KeyboardInterrupt:
    pass


new_sock.close()
print("Connection establish from", addr)

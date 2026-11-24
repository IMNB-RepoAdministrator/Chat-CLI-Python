import socket

import yaml

from shared import get_path, sock_create
from shared.extra.timeout import timeout

SHARED_CONFIG_FILE = get_path.get_shared_path()
ASK_REQUEST = f"Who is Chat-CLI server? {SHARED_CONFIG_FILE["version"]}".encode()
SVRANS_REQUEST = f"I am Chat-CLI server. {SHARED_CONFIG_FILE["version"]}".encode()
CLI_ACK = f"Chat-CLI Client Acknowledge. {SHARED_CONFIG_FILE["version"]}".encode()
TIMEOUT = SHARED_CONFIG_FILE["timeout-length"]

class SvBroadcaster:
    """
    **Description**:
        Instantiate a **Broadcaster** object and automatically bind itself to 0.0.0.0.
        This object contains common method that will be use for the server.
        
    **NOTE**: This is only for handling connection, not the entire application itself.
    """
        
    def __init__(self, shared_cfg_path : str = SHARED_CONFIG_FILE):
        with open(shared_cfg_path, "r") as config_file:
            shared_config = yaml.safe_load(config_file)
    
        self.broadcast_socket, self.broadcast_addr = sock_create.create_UDPsocket(
            (
                "255.255.255.255", 
                shared_config["broadcast-server-port"]
            )
        )
        
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.size = shared_config["packet-size"]
        

    ## Private methods
    @timeout(TIMEOUT, False)
    def _synchronize(self, addr : socket._RetAddress):
        """
        **PRIVATE METHOD**
        
        Initializing handshake and synchronize with client.
        """
        
        self.broadcast_socket.sendto(SVRANS_REQUEST, addr)
        rep_msg = b""
        
        while rep_msg == b"":
            packet = self.broadcast_socket.recvfrom(self.size)
            addr = packet[1]
            rep_msg = packet[0]
            
            if rep_msg == CLI_ACK:
                break
                
            else:
                rep_msg = b""

        return True
            
    ## Public methods
    
    def discover(self):
        """
        Discover client from broadcast.
        """
        
        message = b""
        
        while message == b"":
            packet = self.broadcast_socket.recvfrom(self.size)
            message = packet[0]
            addr = packet[1]
            
            if message == ASK_REQUEST:
                status = self._synchronize(addr)
                
                if status == True:
                    return addr
                
            
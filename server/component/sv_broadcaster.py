import pathlib
import socket
import sys

import yaml

sys.path.append(str(pathlib.Path.cwd())) # Resolve import

from shared.comm.response import response
from shared.config import file_path as get_path
from shared.extra.timeout import timeout
from shared.extra.timeout_receive import timeout_receive
from shared.sock import create_socket as sock_create

SHARED_CONFIG_PATH = get_path.get_shared_path()    

class sv_broadcaster:
    """
    **Description**:
        Instantiate a **Broadcaster** object and automatically bind itself to `broadcast-server-port`.
        This object contains common method that will be use for the server.
        
    **NOTE**: This is only for handling connection, not the entire application itself.
    """
        
    def __init__(self, shared_cfg_path : str = SHARED_CONFIG_PATH):
        with open(shared_cfg_path, "r") as config_file:
            shared_config = yaml.safe_load(config_file)
    
        self.broadcast_socket, self.broadcast_property = sock_create.create_UDPsocket(
            (
                shared_config["broadcast-addr"], 
                shared_config["broadcast-port"]
            )
        )
        
        self.broadcast_socket.bind((self.broadcast_property.addr, self.broadcast_property.port))
        
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.size = shared_config["packet-size"]
        self.TIMEOUT = shared_config["timeout-length"]        
        self.REPEATING_RATE = shared_config["repeating-rate"]
        

    ## Private methods
    
    def _sv_synchronize(self, addr : socket._RetAddress):
        """
        **PRIVATE METHOD**
        
        Initializing handshake and synchronize with client. If not possible, return None.
        """
                    
        @timeout(self.TIMEOUT) # Because you can't pass self attribute from outside for some reason smh.
        def decorated_sync():
            nonlocal addr
            
            while True:
                rep_msg = b""
                
                while rep_msg == b"":
                    self.broadcast_socket.sendto(response("SVRANS_REQUEST"), addr)
                    packet = timeout_receive(self.size, "UDP", self.broadcast_socket, self.REPEATING_RATE)
                    
                    if packet != None:                   
                        rep_msg = packet[0]
                        
                        if rep_msg == response("CLI_ACK"):
                            self.broadcast_socket.sendto(b"", addr)
                            return True
                        
                        else:
                            rep_msg = b""
                            break
                
        return decorated_sync()
            
    ## Public methods

    def broadcast_discover(self):
        """
        Discover client by broadcasting.
        """
        
        message = b""
        
        while message == b"":
            packet = self.broadcast_socket.recvfrom(self.size)
            
            message = packet[0]
            addr = packet[1]
            
            if message == response("ASK_REQUEST") and self._sv_synchronize(addr) != None:
                return addr
            
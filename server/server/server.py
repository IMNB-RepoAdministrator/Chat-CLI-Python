import sys
import pathlib

sys.path.append(str(pathlib.Path().absolute()) + "/server")

from component.sv_broadcaster import sv_broadcaster
from shared.extra.run_only_thread import run_only_thread

class server:    
    """
    Instantiate a "Server" object which represent `server` part in server - client model.
    """
    
    def __init__(self):
        self.broadcaster = sv_broadcaster()
        self.addr_list = {}
    
    ## public methods
        
    def run(self):
        addr = self.broadcaster.broadcast_discover()
        print(f"Connection establish from {addr}.")

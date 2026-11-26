# from server.server.server import server
import pathlib
import sys

sys.path.append(str(pathlib.Path.cwd())) # Resolve import

from shared.extra.run_only_thread import run_only_thread

from .component.sv_broadcaster import sv_broadcaster


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


if __name__ == "__main__":
    chat_server = server()
    server_thread = run_only_thread(chat_server.run)
    
    try:
        server_thread.start()
        server_thread.join()
    
    except KeyboardInterrupt:
        server_thread.terminate()
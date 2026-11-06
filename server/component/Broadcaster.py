from shared import sock_create
import pathlib
import socket
import yaml

SHARED_ABSOLUTE_PATH = "/".join(str(pathlib.Path(__file__).resolve()).split("/")[:-2] + ["shared"])
SHARED_CONFIG_FILE = SHARED_ABSOLUTE_PATH + "/".join(["config", "sharedconfig.yaml"])


class Broadcaster(object):
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
                shared_config["broadcast-server-ip"], 
                shared_config["broadcast-server-port"]
            )
        )
         
        self.size = shared_config["packet-size"]
        
        
    ## Private methods
    
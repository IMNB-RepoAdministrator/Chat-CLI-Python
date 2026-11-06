from shared import sock_create
import yaml
import socket
import pathlib

SERVER_ABSOLUTE_PATH = "/".join(str(pathlib.Path(__file__).parent.resolve()).split("/")[:-1])
SERVER_CONFIG_PATH = SERVER_ABSOLUTE_PATH + "/".join(["config", "serverconfig.yaml"])

SHARED_ABSOLUTE_PATH = "/".join(str(pathlib.Path(__file__).resolve()).split("/")[:-2] + ["shared"])
SHARED_CONFIG_FILE = SHARED_ABSOLUTE_PATH + "/".join(["config", "sharedconfig.yaml"])


class ClientHandler(object):
    """
    **Description**:
        Instantiate a **ClientHandler** object and automatically bind itself to address in config file.
        This object contains common method that will be use for the server.
        
    **NOTE**: This is only for handling connection, not the entire application itself.
    """

    def __init__(self, sv_cfg_path : str = SERVER_CONFIG_PATH, shrd_cfg_path : str = SHARED_CONFIG_FILE):        
        with open(sv_cfg_path, "r") as svr_config_yaml:
            server_config = yaml.safe_load(svr_config_yaml)
        
        with open(shrd_cfg_path, "r") as shr_config_yaml:
            shared_config = yaml.safe_load(shr_config_yaml)
            
        HOST = socket.gethostbyname(socket.gethostname())
        
        self.UDPSock, self.UDPProp = sock_create.create_UDPsocket(
                (
                    server_config["udp-server-ip"] if server_config["udp-server-ip"] != "0.0.0.0" else HOST, 
                    server_config["udp-server-port"]
                )
            )
        
        self.TCPSock, self.TCPProp = sock_create.create_TCPsocket(
                (
                    server_config["tcp-server-ip"] if server_config["tcp-server-ip"] != "0.0.0.0" else HOST, 
                    server_config["tcp-server-port"]    
                )
            )

        self.recv_size = shared_config["packet-size"]
        
        self._server_bind()


    ## Private methods
           
    def _server_bind(self):
        """
        Private methods
        """
        
        self.TCPSock.bind((self.TCPProp.addr, self.TCPProp.port))


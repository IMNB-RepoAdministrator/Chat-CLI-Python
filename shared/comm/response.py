from typing import Literal

import yaml

from ..config import file_path

SHARED_CONFIG_PATH = file_path.get_shared_path()    

def response(response : Literal["ASK_REQUEST", "SVRANS_REQUEST", "CLI_ACK"]):
    with open(SHARED_CONFIG_PATH, "r") as config_file:
        SHARED_CONFIG_FILE = yaml.safe_load(config_file)

        response_list = {
            "ASK_REQUEST" : f"Who is Chat-CLI server? {SHARED_CONFIG_FILE['version']}".encode(),
            "SVRANS_REQUEST" : f"I am Chat-CLI server. {SHARED_CONFIG_FILE['version']}".encode(),
            "CLI_ACK" : f"Chat-CLI Client Acknowledge. {SHARED_CONFIG_FILE['version']}".encode(),
        }
    
    return response_list[response]

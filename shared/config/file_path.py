import pathlib

import yaml

SHARED_ABSOLUTE_PATH = "/".join(str(pathlib.Path(__file__).resolve()).split("/")[:-3])
CURRENT_DIR = f"{SHARED_ABSOLUTE_PATH}/shared/config"

def get_shared_path():
    with open(f"{CURRENT_DIR}/file_path.yaml", "r") as yaml_file:
        path = yaml.safe_load(yaml_file.read())
    
    return SHARED_ABSOLUTE_PATH + path["shared-config-path"]

def get_client_path():
    with open(f"{CURRENT_DIR}/file_path.yaml", "r") as yaml_file:
        path = yaml.safe_load(yaml_file.read())
    
    return SHARED_ABSOLUTE_PATH + path["client-config-path"]

def get_server_path():
    with open(f"{CURRENT_DIR}/file_path.yaml", "r") as yaml_file:
        path = yaml.safe_load(yaml_file.read())
    
    return SHARED_ABSOLUTE_PATH + path["server-config-path"]
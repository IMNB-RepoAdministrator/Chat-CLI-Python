"""
**Description**:
    Shared component for both server and client.

**Note**:
    If you want to deploy to other client or server then copy this folder and the client or server folder server. 
"""

# Changing namespace
from sock import create_socket as sock_create
from model import model_socket as shared_model
from config import file_path as get_path

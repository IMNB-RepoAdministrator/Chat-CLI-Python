"""
    Send data with header (header template is in specs/).
"""

import socket
from typing import Literal

HEADER_TYPE = Literal["broadcast", "send_msg", "send_file"]

def tcp_hsend_all(header_type : HEADER_TYPE, data : str, tcp_sock : socket.socket):
    ...
    
def udp_hsend_all(header_type : HEADER_TYPE, data : str, udp_sock : socket.socket):
    ...
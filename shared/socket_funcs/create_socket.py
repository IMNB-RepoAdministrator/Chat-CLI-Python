from model.model_socket import socket_property
import socket

def create_UDPsocket(addr : tuple[str, int]):
    """
    Create UDP socket.
    
    **NOTE**: This doesn't establish any connection at all, just only create socket.<br>
              You **still** need to do the manual work of connecting and binding.</br>
    """
    
    new_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    properties = socket_property("UDP", addr[0], addr[1])
    return (new_udp_socket, properties)

def create_TCPsocket(addr : tuple[str, int]):
    """
    Create TCP socket.
    
    **NOTE**: This doesn't establish any connection at all, just only create socket.<br>
              You **still** need to do the manual work of connecting and binding.</br>
    """
    
    new_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    properties = socket_property("TCP", addr[0], addr[1])
    return (new_tcp_socket, properties)
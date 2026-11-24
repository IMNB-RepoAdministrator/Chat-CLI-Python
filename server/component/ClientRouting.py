from shared import sock_create
import yaml
import socket
import pathlib

def client_routing(client_socket : socket.socket, message : str):
    ...
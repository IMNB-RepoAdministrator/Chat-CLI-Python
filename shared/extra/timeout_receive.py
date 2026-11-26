import socket
from typing import Literal

from .timeout import timeout


def timeout_receive(size : int, mode : Literal["UDP", "TCP"], socket : socket.socket, duration : float):
    """
    Socket receive with custom timeout duration.
    
    **NOTE**: Should only use for packet that small and could be receive in one single `recv()` or `recvfrom()` call.
    I haven't test for recursive yet so if packet data is corrupted, you should consider checking this.
    """
    
    @timeout(duration)
    def _timeout_recvfrom():
        nonlocal socket, size
        packet = socket.recvfrom(size)
        return packet

    @timeout(duration)
    def _timeout_recv():
        nonlocal socket, size
        packet = socket.recv(size)
        return packet


    if mode == "TCP":
        return _timeout_recv()
    
    else:
        return _timeout_recvfrom()
import pathlib
import socket
import sys

import yaml
from __future__ import annotations
sys.path.append(str(pathlib.Path.cwd()))  # Resolve import

from shared.comm.response import response
from shared.config import file_path as get_path
from shared.extra.timeout import timeout
from shared.extra.timeout_receive import timeout_receive
from shared.sock import create_socket as sock_create

SHARED_CONFIG_PATH = get_path.get_shared_path()


class client_broadcaster:
    """
    **Description**:
        Instantiate a **Client Broadcaster** object to discover the server over LAN
        via UDP broadcast and perform synchronization handshake.

    **NOTE**: This is only for discovering and establishing initial handshake with server,
    not the entire client application itself.
    """

    def __init__(self, shared_cfg_path: str = SHARED_CONFIG_PATH):
        with open(shared_cfg_path, "r") as config_file:
            shared_config = yaml.safe_load(config_file)

        self.broadcast_addr = shared_config["broadcast-addr"]
        self.broadcast_port = shared_config["broadcast-port"]

        self.broadcast_socket, self.broadcast_property = sock_create.create_UDPsocket(
            (self.broadcast_addr, self.broadcast_port)
        )

        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.size = shared_config["packet-size"]
        self.TIMEOUT = shared_config["timeout-length"]
        self.REPEATING_RATE = shared_config["repeating-rate"]

    ## Private methods

    def _cli_synchronize(self, server_addr: tuple[str, int]):
        """
        **PRIVATE METHOD**

        Complete handshake and synchronize with the discovered server.
        Returns True if acknowledged by server, otherwise None.
        """

        @timeout(self.TIMEOUT)
        def decorated_sync():
            nonlocal server_addr

            while True:
                self.broadcast_socket.sendto(response("CLI_ACK"), server_addr)
                packet = timeout_receive(
                    self.size, "UDP", self.broadcast_socket, self.REPEATING_RATE
                )

                if packet is not None:
                    rep_msg, addr = packet[0], packet[1]

                    if addr == server_addr and rep_msg == b"":
                        return True

                    if addr == server_addr and rep_msg == response("SVRANS_REQUEST"):
                        continue

        return decorated_sync()

    ## Public methods

    def broadcast_discover(self):
        """
        Discover server in LAN by sending UDP broadcast packets.
        Returns server address tuple (ip, port) if found, otherwise None.
        """

        @timeout(self.TIMEOUT)
        def decorated_discover():
            while True:
                self.broadcast_socket.sendto(
                    response("ASK_REQUEST"),
                    (self.broadcast_addr, self.broadcast_port),
                )

                packet = timeout_receive(
                    self.size, "UDP", self.broadcast_socket, self.REPEATING_RATE
                )

                if packet is not None:
                    message, addr = packet[0], packet[1]

                    if message == response("SVRANS_REQUEST") and self._cli_synchronize(addr) is True:
                        return addr

        try:
            return decorated_discover()
        finally:
            self.broadcast_socket.close()
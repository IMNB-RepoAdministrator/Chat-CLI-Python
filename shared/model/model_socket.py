from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class socket_property:
    """
    Dataclass model for TCP, UDP socket.
    """
    type : Literal["UDP", "TCP"]
    addr : str
    port : int
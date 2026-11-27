import pathlib
import sys

sys.path.append(str(pathlib.Path.cwd()))  # Resolve import

from shared.extra.run_only_thread import run_only_thread

from .component.client_broadcaster import client_broadcaster


class client:
    """
    Instantiate a "Client" object which represents `client` part in server - client model.
    """

    def __init__(self):
        self.broadcaster = client_broadcaster()

    def run(self):
        addr = self.broadcaster.broadcast_discover()
        if addr is not None:
            print(f"Connection establish from {addr}.")
        else:
            print("Server discovery timed out.")


if __name__ == "__main__":
    chat_client = client()
    client_thread = run_only_thread(chat_client.run)

    try:
        client_thread.start()
        client_thread.join()

    except KeyboardInterrupt:
        client_thread.terminate()
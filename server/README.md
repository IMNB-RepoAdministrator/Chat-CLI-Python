# Server

Specifications and features document for components of server.

## Broadcast

Server will attempt to broadcast itself to entire LAN if `allow-broadcast-found` set to `true`, else it will
just use default `<socket>-server-ip` and `<socket>-server-port` to wait client connect to it. Broadcast address config can be found in `shared/config/sharedconfig.yaml`. 

After found then client and server will use this address to initialize handshake and encryption if `allow-authentication`, `allow-encrytion-file` and `allow-encrytion-chat` set to `true` or else it will just connect client to server directly.

Default config:

- Broadcast address: `0.0.0.0`
- Broadcast port: `28010`

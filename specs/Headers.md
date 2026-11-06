# Headers

Compile list of headers for client and server.

**Server broadcast send** (Size less than $4096$ bytes):

```
Type: Broadcast /r/n
Identify: Server /r/n
Host: <Server local IP>, <Server port> /r/n
Data-Size: <Data size> /r/n/r/n
```

**Client broadcast send** (Size less than $4096$ bytes):

```
Type: Broadcast /r/n
Identify: Client /r/n
Host: <Client local IP>, <Client port> /r/n
Data-Size: <Data size> /r/n/r/n
```
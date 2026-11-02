# Chat server project

## Specification

> [!NOTE]
> This could be consider as requirements for the chat server.

- Using **Client - Server** model.
- Support handling multiple users at the same time.
- Support transfering files and messages to one or multiple users.
- Has basic authentification for security.

## Component

There are 2 mains component:

- **Server**: Handling between clients:
  - Transfering data (messages, user's status and files). **$\leftarrow$ Main work.**
  - Establishing connections. **$\leftarrow$ Main work.**
  - Authenticaion and encryption (mainly user's password). **$\leftarrow$ Main work.**
  - Discovering users in LAN. **$\leftarrow$ Main work.**
  - ... **$\leftarrow$ More work could be in here.**

- **Client**: Interacting with server other clients:
  - Updating own's status to server (<b style="color : #ff0000">Offline</b>/<b style="color : #00ff00">Online</b>/<b style="color : #ffff00">Idle</b>)
  - Able to discover server through broadcast.
  - Able to use command to use application and interact with other clients. Require command:
    - **/list**: Listing available clients in the current server.
    - **/chat \<name|id number>**: Establish a chat session to other client.
      - **/send \<file|folder>**: Send file or folder to the other client.
    - **/send \<name|id number> \<file|folder>**: Send file or folder to other without establishing chat session.
    - **/leavechat**: Leave chat session.
    - **/leave**: Leave the server.
    - **/setstatus \<status_option>**: Set status from given status:
      - <b style="color : #00ff00">Online</b>
      - <b style="color : #ff0000">Offline</b>
      - <b style="color : #ffff00">Idle</b>
    - **/help**: Print help message.
    - **/quit**: Quit the app (not just disconnecting from chat server).

## Work

There are 3 mains area that need to work on:

- **Server**: Building server with features that is require in [Component](#component)

- **Client**: Building command-line interface applications with required features in [Component](#component).

- **Test**: Main tasks:
  - Check performance of server and client (**Latency**/**Resource Usage**).
  - Check if there are errors or courruptions in files sending and messages sending.
  - Check if server and client operate properly.

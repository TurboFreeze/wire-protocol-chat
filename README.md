# chat-app

Chat application with custom wire protocol. Instructions for usage and installation are in this important README file while an overview of the design is contained in DESIGN.pdf and the rest of the pydoc documentation is in the `doc` directory.

## INSTALLATION AND LAUNCH

### Requirements

Requires `Python v2.7`. Designed for Linux/MacOS operating systems. Multiple clients in separate terminals can connect to the same server. The client and server can both run on the same machine **OR** clients on the local machine terminal can connect to `262.squire.io:2620`, where a server instance is currently running.

### Download

Hosted on code.harvard.edu repo. Clone or download from https://code.harvard.edu/jah9590/chat-app.

### Client

Open a new Terminal/command line instance for each client instance. Set the `client` directory as the working directory. Run the exact following command in the client Terminal:
```
python2.7 262.squire.io 2620
```
Alternatively, you can use an IP address of your choice for a machine where the server is running (however, do this at your own risk; we only guarantee support for `262.squire.io:2620`).

### Server

Open a new Terminal/command line instance for the server. Set the `server` directory as the working directory and run `./start.sh`.

## USAGE

Whether logged in or not, the user in the client window can enter 0 to exit the program. The user can enter 3 to list all users stored by the server. Listing users takes an optional wildcard, such that only usernames containing the wildcard as a subsequence are returned.

### Not Logged In

If not logged in, select 2 to first create an account. The user will be redirected to the same home page after creating an account, where the user can login or create another account.

Select 1 to login to the account that was just created, or into an account that was previously created.

### Logged In

Once logged in, entering 1 can send a message to the desired recipient. The user will be prompted to enter a username for an existing user and the message itself.

The logged in user can also choose to delete their own account. Selecting `y` for yes forces deletion regardless of whether or not there are pending messages for that user, while `n` will only delete if the message queue for that user is empty.

## Technical Overview

For technical details about this software, please refer to the included `pydoc` documentation in the `doc` directory. A **complete wire protocol** was defined and implemented (see op codes in the documentation). Communication between machines is achieved using socket connections. Every wire message is packed and unpacked using the corresponding utility from Python's `struct` module: `pack()` for sending messages and `unpack()` for receiving messages according to the wire protocol.

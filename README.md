# chat-app

Chat application with custom wire protocol. Instructions for usage and installation are in this important README file while an overview of the design is contained in DESIGN.pdf and the rest of the pydoc documentation is in the `doc` directory.

## INSTALLATION AND LAUNCH

### Requirements

Requires `Python v2.7`. Designed for Linux/MacOS operating systems. Multiple clients in separate terminals can connect to the same server, all on the same machine.

### Download

Hosted on code.harvard.edu repo. Clone or download from https://code.harvard.edu/jah9590/chat-app.

### Client

Open a new Terminal/command line instance for each client instance. Set the `client` directory as the working directory and run `./start.sh`.

### Server

Open a new Terminal/command line instance for the server. Set the `server` directory as the working directory and run `./start.sh`.

## USAGE

Whether logged in or not, the user in the client window can enter 0 to exit the program. The user can enter 3 to list all users stored by the server (with an optional wildcard for matching desired usernames).

### Not Logged In

If not logged in, select 2 to first create an account. The user will be redirected to the same home page after creating an account, where the user can login or create another account.

Select 1 to login to the account that was just created, or into an account that was previously created.

### Logged In

Once logged in, entering 1 can send a message to the desired recipient. The user will be prompted to enter a username for an existing user and the message itself.

The logged in user can also choose to delete their own account. Selecting `y` for yes forces deletion regardless of whether or not there are pending messages for that user, while `n` will only delete if the message queue for that user is empty.

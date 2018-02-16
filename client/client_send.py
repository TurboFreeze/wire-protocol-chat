from client_receive import *
from protocol_strings import *
from struct import pack, unpack
import thread

def login(connection):
    """
    Send user request to login to an already existing account based on the provided username.
    """
    # Get username
    username = raw_input('Login requires a username: ')
    while len(username) > 32:
        username = raw_input('Username too long (max 32 alphanumeric characters). Please try again: ')

    # Pack wire message and send it
    msg = pack('!I', LOGIN_REQUEST) + pack('!32s', username)
    send_wire_message(connection, msg)
    return

def create_account(connection):
    """
    Send a request to creating a new account with the username provided by the user.
    """
    # Get username
    username = raw_input('Registering a new account requires a new unique username (max 32 characters): ')
    while len(username) > 32:
        username = raw_input('Username too long (max 32 characters). Please try again: ')

    # Pack wire message and send it
    msg = pack('!I', CREATE_ACCOUNT) + pack('!32s', username)
    send_wire_message(connection, msg)
    return

def get_list_accounts(connection):
    """
    Send a request for the list of all accounts, with an optional wildcard for matching account usernames.
    """
    # Get the wildcard
    wildcard = raw_input('Enter a wildcard (max 32 characters) for retrieving usernames (optional) and hit enter: ')

    # Pack wire message and send it
    msg = pack('!I', LIST_ACCOUNTS) + pack('!32s', wildcard)
    send_wire_message(connection, msg)
    return

def send_message(connection):
    """
    Send the provided message to the specified recipient from this account
    """
    # Get the username of the intended recipient
    recipient = raw_input('Recipient: ')
    while len(recipient) > 32:
        recipient = raw_input('Username too long (max 32 characters). Please try again: ')

    # Get the message
    content = raw_input('Message Content (max 100 characters): ')
    while len(content) > 100:
        content = raw_input('Message too long (max 100 characters). Please try again: ')

    msg = pack('!I', SEND_MESSAGE) + pack('!32s', recipient) + pack('!100s', content)
    send_wire_message(connection, msg)
    return

def delete_account(connection, username):
    """
    Send a request to delete the current account, with user option of forcing deletion
    """
    # Get user option choice
    force_bool = None
    while force_bool == None:
        force = raw_input('Force deletion? [y/n]: ')
        force = force.strip()
        # Parse the argument
        if force == 'y':
            force_bool = True
        elif force == 'n':
            force_bool = False
        else:
            print "Not recognized. Enter 'y' for yes, 'n' for no."

    # Send the wire message
    msg = pack('!I', DELETION_REQUEST) + pack('!32s', username) + pack('?', force_bool)
    send_wire_message(connection, msg)
    return

def send_wire_message(socket, wire_message):
    try:
        socket.send(wire_message)
    except:
        print 'Unable to send message; connection closed'
        sys.exit()
    return

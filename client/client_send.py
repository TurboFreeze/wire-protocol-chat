from protocol_strings import *
from struct import pack, unpack

def login(connection):
    username = raw_input('Login requires a username (max 8 alphanumeric characters): ')
    while len(username) > 10:
        username = raw_input('Username too long (max 8 alphanumeric characters). Please try again: ')

    msg = pack('!I', CREATE_ACCOUNT) + pack('!8p', username)
    send_wire_message(connection, msg)
    return

def create_account(connection):
    pass

def list_accounts(connection):
    pass

def send_message(connection):
    pass

def delete_account(connection):
    pass

def send_wire_message(connection, wire_message):
    try:
        print 'Sending ' + wire_message
        connection.send(wire_message)
    except:
        print 'Unable to send message; connection closed'
        sys.exit()
    return

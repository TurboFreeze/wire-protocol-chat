from protocol_strings import *
from struct import pack, unpack

def create_success(content):
    """
    Response to user if successfully created user
    :param content: contents of the packed wire message received from server
    """
    print 'Account creation was successful for: ' + unpack('!32s', content[4:])[0]
    print 'You can now login or create another account'
    return

def create_failure(content):
    """
    Response to user if user creation unsuccessful
    :param content: contents of the packed wire message received from server
    """
    print 'Account creation was not successful for: ' + unpack('!32s', content[4:])[0]
    print 'This username might already be taken.'
    return

def login_success(content):
    """
    Response to user if login successful
    :param content: contents of the packed wire message received from server
    """
    print 'Successfully logged in as: ' + unpack('!32s', content[4:])[0]
    return

def login_failure(content):
    """
    Response to user if login unsuccessful
    :param content: contents of the packed wire message received from server
    """
    print 'Login unsuccessful. Make sure the user exists and try again.'
    return

def out_list_accounts(content):
    """
    Response to user of list of accounts retrieved
    :param content: contents of the packed wire message received from server
    """
    wildcard = unpack('!32s', content[4:36])[0]
    number = unpack('!I', content[36:40])[0]
    print 'The wildcard used was: ' + wildcard
    print 'The list of users found with this wildcard are:'
    # Loop through all usernames packed into the wire protocol
    for i in range(number):
        start = 40 + i * 32
        end = 40 + (i + 1) * 32
        print unpack('!32s', content[start:end])[0]
    return

def message_success(content):
    """
    Response to user upon successful sending of message
    :param content: contents of the packed wire message received from server
    """
    pass

def message_received(content):
    """
    Output message to client terminal upon receiving a message
    :param content: contents of the packed wire message received from server
    """
    recipient = unpack('!32s', content[4:36])
    message = unpack('!100s', content[36:])[0]
    print('\n[MESSAGE RECEIVED]: ' + message)
    return

def message_failure(content):
    """
    Response to user if a message could not be delivered
    :param content: contents of the packed wire message received from server
    """
    print 'Receiving user does not exist.'
    return

def message_pending(content):
    """
    Response to user if message was successfully queued
    :param content: contents of the packed wire message received from server
    """
    print 'The message has been sent and the recipient will see it immediately/the next they log in.'
    return

def deletion_success(content):
    """
    Response to user if deletion of account was successful
    :param content: contents of the packed wire message received from server
    """
    print 'Account deletion was successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account no longer exists. Goodbye!'
    return

def deletion_failure(content):
    """
    Response to user if deletion of account could not be performed
    :param content: contents of the packed wire message received from server
    """
    print 'Account deletion was not successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account still exists. You can only delete your own account and you must be logged in.'
    return

from protocol_strings import *
from struct import pack, unpack

def create_success(content):
    """
    Response to user if successfully created user
    """
    print 'Account creation was successful for: ' + unpack('!32s', content[4:])[0]
    print 'You can now login or create another account'
    return

def create_failure(content):
    print 'Account creation was not successful for: ' + unpack('!32s', content[4:])[0]
    print 'This username might already be taken.'
    return

def login_success(content):
    print 'Successfully logged in as: ' + unpack('!32s', content[4:])[0]
    return

def login_failure(content):
    print 'Login unsuccessful. Make sure the user exists and try again.'
    return

def out_list_accounts(content):
    wildcard = unpack('!32s', content[4:36])[0]
    number = unpack('!I', content[36:40])[0]
    print 'The wildcard used was: ' + wildcard
    print 'The list of users found with this wildcard are:'
    for i in range(number):
        start = 40 + i * 32
        end = 40 + (i + 1) * 32
        print unpack('!32s', content[start:end])[0]
    return

def message_success(content):
    pass

def message_received(content):
    recipient = unpack('!32s', content[4:36])
    message = unpack('!100s', content[36:])[0]
    print('\n[MESSAGE RECEIVED]: ' + message)
    return

def message_failure(content):
    print 'Receiving user does not exist.'
    return

def message_pending(content):
    print 'The message has been sent and the recipient will see it immediately/the next they log in.'
    return

def deletion_success(content):
    print 'Account deletion was successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account no longer exists. Goodbye!'
    return

def deletion_failure(content):
    print 'Account deletion was not successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account still exists. You can only delete your own account and you must be logged in.'
    return

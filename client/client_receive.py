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
    pass

def message_success(content):
    pass

def message_failure(content):
    pass

def message_pending(content):
    pass

def deletion_success(content):
    print 'Account deletion was successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account no longer exists. Goodbye!'
    return

def deletion_failure(content):
    print 'Account deletion was not successful for: ' + unpack('!32s', content[4:])[0]
    print 'This account still exists. You can only delete your own account and you must be logged in.'
    return

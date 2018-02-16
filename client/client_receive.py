from protocol_strings import *
from struct import pack, unpack

def create_success(content):
    """
    Response to user if successfully created user
    """
    print 'Account creation was successful for: '
    print 'You can now login or create another account'

def create_failure(content):
    print 'Account creation was not successful for: '
    print 'This username might already be taken.'

def login_success(content):
    pass

def login_failure(content):
    pass

def out_list_accounts(content):
    pass

def message_success(content):
    pass

def message_failure(content):
    pass

def message_pending(content):
    pass

def deletion_success(content):
    pass

def deletion_failure(content):
    pass

from protocol_strings import *

class Model_262():
    """TODO documentation"""
    
    controller = None
    
    def __init__(self, controller):
        # TODO note the cyclic relationship between model and controller.
        # Double check that it is justified.
        print "initting"
        self.controller = controller
        # TODO
    
    
    def handle(commandstr, payload):
        # python doesn't have switch statements :(
        
        print "Model received a command string and a payload(?)"
        print commandstr
        print payload
        
        if commandstr == CREATE_ACCOUNT:
            # The server has received a request to create an account
            # we must first check that the account does not already exist,
            # then tell the controller to fire off a CREATION_RESPONSE 
            # TODO
            pass
        
        elif commandstr == LOGIN_REQUEST:
            # The server has received a request to log in.
            # check the payload to make sure the username exists,
            # (handle already logged in), and execute a login in the model.
            # Then tell the controller to fire off a LOGIN_RESPONSE
            # if there are queued messages for this user, deliver them.
            # TODO
            pass
        
        elif commandstr == LIST_ACCOUNTS:
            # The server has received a request to LIST_ACCOUNTS,
            # with some wildcard. Process the request and tell the controller to
            # fire off a ACCOUNT_LIST message with the relevant data
            # TODO
            pass
        
        elif commandstr == SEND_MESSAGE:
            # The server has received a request to send a message to some user
            # from some user. Check the payload for A) correct "from" user,
            # B) correct "to" user, and C) "to" user login status
            # if "to" user is logged in, tell controller to fire off 
            # DISTRIBUTE_MESSAGE. (doesn't count until we get a
            # MESSAGE_RECEIPT confirmation)
            # otherwise, queue the message.
            # After all this is done, tell the controller to fire a 
            # MESSAGE_STATUS_RESPONSE to the "from" user with
            # the relevant payload data
            # TODO
            pass
        
        elif commandstr == MESSAGE_RECEIPT:
            # TODO
            pass
        
        elif commandstr == ACCOUNT_DELETION_REQUEST:
            # A user has requested to delete an account.
            # if this user is the owner of the account, and there are no 
            # pending messages for him/her, execute and send a 
            # ACCOUNT_DELETION_RESPONSE
            #
            # If there are pending messages, but the "force" flag is included 
            # in the payload, execute and send a 
            # ACCOUNT_DELETION_RESPONSE
            #
            # If there are pending messages and the "force" flag is not present,
            # return ACCOUNT_DELETION_RESPONSE with the relevant 
            # warning and do not delete.
            pass
        
        else:
            # TODO default
            print "error"
            pass
        
        
        
        
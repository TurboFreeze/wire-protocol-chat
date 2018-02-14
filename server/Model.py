from protocol_strings import *
from Store import Store

class Model_262():
    """TODO documentation"""
    
    controller = None
    data = None
    
    def __init__(self, controller):
        # TODO note the cyclic relationship between model and controller.
        # Double check that it is justified.
        
        print "Initializing Model..."
        self.controller = controller
        self.data = self.load_data()
    
    # TODO periodically check for and send pending messages to logged-in accounts
    # watch out for double sends if we haven't received a confirmation yet.
    
    
    # takes in a command string (protocol_strings.py) and a corresponding
    # payload (which may have to be pre-processed somewhat by the Controller
    # to preserve modularity. Should be able to feed directly 
    # into self.data dictionaries)
    def interpret(commandstr, payload, session_id):
        
        # python doesn't have switch statements :(
        
        print "Model received a command string and a payload(?)"
        print commandstr
        print payload
        
        if commandstr == CREATE_ACCOUNT:
            # The server has received a request to create an account
            # we must first check that the account does not already exist,
            # then tell the controller to fire off a CREATION_RESPONSE 
            
            if self.data.usernames.has_key(payload["username"]):
                # Error: username already exists
                # TODO tell controller to fire a CREATION_RESPONSE message
                # with payload "failure"/"username taken" or whatever
                pass
            else:
                self.data.usernames[payload["username"]] = True 
                # TODO is there any other data we want to store?
            
                # TODO tell controller to fire a CREATION_RESPONSE message
                # with payload "success"
        
        elif commandstr == LOGIN_REQUEST:
            # The server has received a request to log in.
            # check the payload to make sure the username exists,
            # (handle already logged in), and execute a login in the model.
            # Then tell the controller to fire off a LOGIN_RESPONSE
            # if there are queued messages for this user, deliver them.
            
            if self.data.usernames.has_key(payload):
                if self.data.active_sessions[payload["username"]] == session_id:
                    # TODO already logged in, just return success?
                    pass
                else:
                    self.data.active_sessions[payload["username"]] = session_id
                    
                    if self.data.pending_messages.has_key(payload["username"]):
                        # TODO load and fire pending messages
                        pass
                    else:
                        pass
                        # TODO controller fire a LOGIN_RESPONSE "success" payload
            else:
                # TODO controller fire a LOGIN_RESPONSE "failure" payload
                pass
        
        elif commandstr == LIST_ACCOUNTS:
            # The server has received a request to LIST_ACCOUNTS,
            # with some wildcard. Process the request and tell the controller to
            # fire off a ACCOUNT_LIST message with the relevant data
            
            account_list = []
            for key, data in enumerate(self.data.usernames):
                # TODO if username matches wildcard:
                account_list.append(key)
            
            # TODO controler fire ACCOUNT_LIST with payload username list
            
        
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
            from_user = self.data.usernames[payload["from"]]
            if exists(from_user) and logged_in(from_user):
                # "from" user is OK
                to_user = self.data.usernames[payload["to"]]
                if exists(to_user):
                    if logged_in(to_user):
                        # TODO recipient exists and is logged in, fire mensaje
                        pass
                    else:
                        # TODO recipient exists but is not logged in, queue mensaje
                        if self.data.pending_messages.has_key(to_user):
                            self.data.pending_messages[to_user].append(payload["message"])    
                        else:
                            self.data.pending_messages[to_user] = [payload["message"]]
                    
                else:
                    # TODO recipient doesn't exist, fire controller
                    pass
            
            pass
        
        elif commandstr == MESSAGE_RECEIPT:
            # client confirms receipt of message. If the message was in the
            # pending pool, delete it.
            if pending_messages.has_key(payload["username"]):
                pending_messages[payload["username"]].remove(payload["msg_id"]) # TODO
            
        
        elif commandstr == ACCOUNT_DELETION_REQUEST:
            # A user has requested to delete the account
            # if there are no pending messages for him/her, execute and send a 
            # ACCOUNT_DELETION_RESPONSE
            #
            # If there are pending messages, but the "force" flag is included 
            # in the payload, execute and send a 
            # ACCOUNT_DELETION_RESPONSE
            #
            # If there are pending messages and the "force" flag is not present,
            # return ACCOUNT_DELETION_RESPONSE with the relevant 
            # warning and do not delete.
            
            forced = payload["forced"] # True/False
            
            if pending_messages.has_key(payload["username"]) and len(pending_messages[payload["username"]]) > 0:
                # there are pending messages.
                if forced:
                    pending_messages[payload["username"]] = None
                    usernames[payload["username"]] = None
                    active_sessions[payload["username"]] = None
                    # TODO fire successful deletion?
                else:
                    # TODO fire deletion error - you have pending messages
                    pass
            else:
                # TODO No pending messages, go ahead with deletion
                pass
        
        else:
            # TODO default
            print "error"
            pass
        
        
        
    def load_data(self):
        # TODO if we want to persist data, 
        # here's where it would be loaded into memory.
        
        return Store(None)
        
    
    def exists(self, username):
        return self.data.usernames.has_key(username)
    
    def logged_in(self, username, session_id):
        return self.data.active_sessions[username] == session_id
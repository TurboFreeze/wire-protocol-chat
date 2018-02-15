from protocol_strings import *
from Store import Store
from Wire_Message import Wire_Message
import re # regex for ACCOUNT_LIST

class Model_262():
    """TODO documentation"""
    
    data = None
    
    def __init__(self):
        self.data = Store(None)
        
    
    # takes in a Wire_Message object and returns an optional Wire_Message object
    # for the controller to deal with.
    def interpret(self, msg, session_id):
        ret_payload = {}
        
        # python doesn't have switch statements :(
        if msg.header == CREATE_ACCOUNT:
            # The server has received a request to create an account
            # we must first check that the account does not already exist,
            # then tell the controller to fire off a CREATION_RESPONSE 
            
            if self.data.usernames.has_key(msg.user()):
                # Error: username already exists
                ret_payload["username"] = msg.user()
                return Wire_Message(CREATE_FAILURE, ret_payload)
            else:
                self.data.usernames[msg.user()] = True 
                ret_payload["username"] = msg.user()
                return Wire_Message(CREATE_SUCCESS, ret_payload)

        elif msg.header == LOGIN_REQUEST:
            # The server has received a request to log in.
            # check the payload to make sure the username exists,
            # (handle already logged in), and execute a login in the model.
            # Then tell the controller to fire off a login response
            # if there are queued messages for this user, deliver them.
            
            if self.data.usernames.has_key(msg.user()):
                # user already has an account, no problem just log 'em in
                if (self.data.active_sessions.has_key(msg.user()) and 
                    self.data.active_sessions[msg.user()] == session_id):
                    # user was already logged in, just return success.
                    ret_payload["username"] = msg.user()
                    return Wire_Message(LOGIN_SUCCESS, ret_payload)
                else:
                    # user was not already logged in, let's update their session
                    self.data.active_sessions[msg.user()] = session_id
                    
                    if self.data.pending_messages.has_key(msg.user()):
                        # TODO load and fire pending messages?
                        # or just let the queue checker handle it?
                        pass
                    else:
                        # no pending messages, just return success
                        ret_payload["username"] = msg.user()
                        return Wire_Message(LOGIN_SUCCESS, ret_payload)
                        
            else:
                # user does not have an account! return failure.
                ret_payload["username"] = msg.user()
                return Wire_Message(LOGIN_FAILURE, ret_payload)
        
        elif msg.header == LIST_ACCOUNTS:
            # The server has received a request to LIST_ACCOUNTS,
            # with some wildcard. Process the request and tell the controller to
            # fire off a ACCOUNT_LIST message with the relevant data
            
            account_list = []
            for key in self.data.usernames.keys():
                if re.match(msg.payload["wildcard"], key) != None:
                    account_list.append(key)
            
            ret_payload["accounts"] = account_list
            ret_payload["wildcard"] = msg.payload["wildcard"]
            return Wire_Message(ACCOUNT_LIST, ret_payload)
            
        
        elif msg.header == SEND_MESSAGE:
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
            from_user = msg.payload["from"]
            if self.exists(from_user) and self.logged_in(from_user, session_id):
                to_user = msg.payload["to"]
                if self.exists(to_user):
                    # to simplify, all messages are queued. Then the controller
                    # just asks for what messages to send every tick.
                    # the model handles logged in/not logged in situations,
                    # and only removes a message from the queue when it gets
                    # a confirmation that it has been received.
                    
                    self.data.queue_message(from_user, to_user, msg.payload["message"])
                    
                    # TODO message hash?
                    ret_payload["message"] = msg.payload["message"]
                    return Wire_Message(MESSAGE_PENDING, ret_payload)
                    
                else:
                    # recipient doesn't exist, fire controller
                    ret_payload["to"] = to_user
                    ret_payload["from"] = from_user
                    return Wire_Message(MESSAGE_FAILURE, ret_payload)
            else:
                # improper sender - isn't logged in!
                # (includes "account doesn't exist")
                ret_payload["username"] = msg.user()
                return Wire_Message(LOGIN_FAILURE, ret_payload)
            
        
        elif msg.header == MESSAGE_RECEIPT:
            # client confirms receipt of message. If the message was in the
            # pending pool, delete it.
            self.data.dequeue_message(msg.payload["from_user"], 
                                      msg.user(), 
                                      msg.payload["message"])
            
        
        elif msg.header == DELETION_REQUEST:
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
            
            forced = False
            if msg.payload.has_key("forced"):
                forced = msg.payload["forced"]
            
            
            if (self.data.pending_messages.has_key(msg.user()) and 
                len(self.data.pending_messages[msg.user()]) > 0):
                # there are pending messages.
                if forced:
                    self.data.pending_messages[msg.user()] = None
                    self.data.usernames[msg.user()] = None
                    self.data.active_sessions[msg.user()] = None

                    ret_payload["username"] = msg.user()
                    return Wire_Message(DELETION_SUCCESS, ret_payload)
                else:
                    # Error! you have pending messages.
                    ret_payload["username"] = msg.user()
                    return Wire_Message(DELETION_FAILURE, ret_payload)
                    
            else:
                # No pending messages, go ahead with deletion
                self.data.pending_messages[msg.user()] = None
                self.data.usernames[msg.user()] = None
                self.data.active_sessions[msg.user()] = None

                ret_payload["username"] = msg.user()
                return Wire_Message(DELETION_SUCCESS, ret_payload)
        
        else:
            # TODO default
            print "error"
            pass
        
    
    # checks all pending messages and returns an ordered list of messages that
    # still have to be sent out/haven't been confirmed yet.
    def get_pending_messages(self):
        ret_list = []
        for key in self.data.pending_messages.keys():
            for message in self.data.pending_messages[key]:
                payload = {}
                payload["username"] = key
                payload["message"] = message
                ret_list.append(Wire_Message(DISTRIBUTE_MESSAGE, payload))
        
        return ret_list
    
    def exists(self, username):
        return self.data.usernames.has_key(username)
    
    def logged_in(self, username, session_id):
        return self.data.active_sessions[username] == session_id
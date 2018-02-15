

class Store():
    """TODO documentation"""
    
                            # key: value
    usernames          = {} # username: True/False
    active_sessions    = {} # username: session_id
    pending_messages   = {} # username: [msg1, msg2, ...]
    
    
    
    def __init__(self, path):
        if path != None:
            # TODO load serialized data?
            pass
        else:
            # TODO other setup?
            pass
    
    
    # TODO right now from_user isn't included, since it isn't in the spec
    # and complicates things. If a user wanted to be identified, they could 
    # include their username in a message. Otherwise it's anonymous.
    def queue_message(self, from_user, to_user, message):
        if self.pending_messages.has_key(to_user):
            self.pending_messages[to_user].append(message)    
        else:
            self.pending_messages[to_user] = [message]
    
    
    def dequeue_message(self, from_user, to_user, message):
        if self.pending_messages.has_key(to_user):
            self.pending_messages[to_user].remove(message) # lot of string matching :(
        else:
            # TODO handle faulty dequeue?
            pass
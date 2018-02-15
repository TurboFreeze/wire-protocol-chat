

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
    
    
    def queue_message(user, message):
        if pending_messages.has_key(to_user):
            pending_messages[to_user].append(message)    
        else:
            pending_messages[to_user] = [message]
    
    
    def dequeue_message(user, message):
        if pending_messages.has_key(user):
            pending_messages[user].remove(message) # lot of string matching :(
        else:
            # TODO handle faulty dequeue?
            pass
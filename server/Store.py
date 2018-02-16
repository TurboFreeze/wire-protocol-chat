

class Store():
    """
    Class to store the core internal data of the server. For now this is memory-only.
    :param path: The location of the data on disk to load (unused)
    """
    
                            # key: value
    usernames          = {} # username: True/False
    active_sessions    = {} # username: session_id
    pending_messages   = {} # username: [msg1, msg2, ...]
    
    
    
    def __init__(self, path):
        if path != None:
            # TODO: this is where we would load stored data if we had to persist
            # it wasn't in the spec, so is not implemented at this point
            pass
        else:
            pass
    
    
    
    def queue_message(self, from_user, to_user, message):
        """
        Add a message to the pending_messages structure
        :param from_user: message sender (unused)
        :param to_user: message recipient
        :param message: message content
        """
        # Note: right now from_user isn't included, since it isn't in the spec
        # and complicates things. If a user wanted to be identified, they could 
        # include their username in a message. Otherwise it's anonymous.
        if self.pending_messages.has_key(to_user):
            self.pending_messages[to_user].append(message)    
        else:
            self.pending_messages[to_user] = [message]
    
    
    def dequeue_message(self, from_user, to_user, message):
        """
        Remove a pending message that has been successfully delivered 
        (or is no longer necessary)
        :param from_user: original message sender (unused)
        :param to_user: message recipient
        :param message: message content
        """
        if self.pending_messages.has_key(to_user):
            self.pending_messages[to_user].remove(message) # lot of string matching :(
        else:
            # TODO: handle missed dequeue request (in an ideal world this would 
            # be implemented, but for now it is not mission-critical)
            pass
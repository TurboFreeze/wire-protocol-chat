
class Wire_Message():
    """
    Class to standardize Wire Protocol messages internally.
    :param header: Wire Protocol header (from protocol_strings)
    :param payload: message content
    """
    
    header = None
    payload = {}
    
    def __init__(self, header, payload):
        self.header = header
        self.payload = payload
    
    def user(self):
        return self.payload['username']
    
    def __str__(self):
        print self.username()
        print header
        print payload
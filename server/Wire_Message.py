
class Wire_Message():
    # TODO documentation
    
    header = None
    payload = {}
    
    # header is a protocol_strings element
    def __init__(self, header, payload):
        self.header = header
        self.payload = payload
    
    def user(self): # TODO is this the best way to do this?
        return self.payload["username"]
    
    def __str__(self):
        print self.username()
        print header
        print payload
'''
    TODO Documentation
    some code from 
            binarytides.com/python-socket-server-code-example/
            docs.python.org/2/howto/sockets.html
'''

from Model import Model_262
from protocol_strings import *
import socket
import sys


class Controller():
    # TODO all this socket stuff will have to be cleaned up 
    # and documented once the client is functional.
    
    
    model = None
    server_socket = None
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.model = Model_262()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
 
        # Bind socket to local host and port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.server_socket.bind((self.host, self.port))
        except socket.error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
     
        print 'Socket bind complete'
         
        # Start listening on socket
        self.server_socket.listen(10)
        print 'Socket now listening'
 
        # now keep talking with the client
        while 1:
            # wait to accept a connection - blocking call
            (clientsocket, address) = self.server_socket.accept()
            
            # TODO thread out connection?
            # ct = client_thread(clientsocket)
            # ct.run()
            print 'Connected with ' + address[0] + ':' + str(address[1])
             
        self.server_socket.close()
    
    
    # TODO periodically check the model for pending messages to logged-in accounts
    # watch out for double sends if we haven't received a confirmation yet.
    
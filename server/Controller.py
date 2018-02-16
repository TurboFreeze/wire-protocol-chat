'''
    TODO Documentation
    some code from
            binarytides.com/python-socket-server-code-example/
            docs.python.org/2/howto/sockets.html
'''

from Model import Model_262
from Wire_Message import Wire_Message
from protocol_strings import *
from struct import pack, unpack
import socket
import sys
import thread


def send_wire_message(connection, wire_message):
    try:
        connection.send(wire_message)
    except:
        print 'Unable to send message'
    return

def prep_response(content):
    response = pack('!I', content.header)
    if content.header == CREATE_SUCCESS or content.header == CREATE_FAILURE:
        response += pack('!32s', content.payload['username'])
    if content.header == LOGIN_SUCCESS or content.header == LOGIN_FAILURE:
        response += pack('!32s', content.payload['username'])
    if content.header == DELETION_SUCCESS or content.header == DELETION_FAILURE:
        response += pack('!32s', content.payload['username'])
    return response

def manage(connection, loc, session_id, model):
    while True:
        try:
            received = connection.recv(1024)
        except:
            # Connection down
            thread.exit()

        if len(received) >= 4:
            header = unpack('!I', received[0:4])[0]
            payload = {}
            if header == CREATE_ACCOUNT:
                payload['username'] = unpack('!32s', received[4:])[0]
            elif header == LOGIN_REQUEST:
                payload['username'] = unpack('!32s', received[4:])[0]
            elif header == LIST_ACCOUNTS:
                pass
            elif header == SEND_MESSAGE:
                pass
            elif header == DELETION_REQUEST:
                payload['username'] = unpack('!32s', received[4:36])[0]
                payload['forced'] = unpack('?', received[36:])[0]
            else:
                print 'Unrecognized protocol operation'

            response = prep_response(model.interpret(Wire_Message(header, payload), session_id))
            send_wire_message(connection, response)

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

        counter = 0

        # now keep talking with the client
        while 1:

            # wait to accept a connection - blocking call
            (clientsocket, address) = self.server_socket.accept()

            lock = thread.allocate_lock()
            thread.start_new_thread(manage, (clientsocket, lock, counter, self.model))
            print 'Connected with ' + address[0] + ':' + str(address[1])
            counter += 1

        self.server_socket.close()


    # TODO periodically check the model for pending messages to logged-in accounts
    # watch out for double sends if we haven't received a confirmation yet.

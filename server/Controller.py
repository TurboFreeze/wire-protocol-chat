"""
    This file contains helper functions and the main Controller class for the 
    messaging server. The Controller opens the server's socket and handles
    incoming connections from clients. It adheres to the wire protocol,
    updating the model and continually distributing pending messages.
    
    Note: some code from
            binarytides.com/python-socket-server-code-example/
            docs.python.org/2/howto/sockets.html
"""

from Model import Model_262
from Wire_Message import Wire_Message
from protocol_strings import *
from struct import pack, unpack
import socket
import sys
import thread
import time


def send_wire_message(connection, wire_message):
    """
    Reusable helper method to encapsulate sending of wire messages
    :param connection: connection to client to send wire message to
    :param wire_message: contents of the packed wire message to be sent to client
    """
    try:
        connection.send(wire_message)
    except:
        print 'Unable to send message'
    return

def prep_response(content):
    """
    Prepare server's response back to client correctly according to the wire protocol
    :param content: Wire_Message object to be processed into wire message
    :return: content object data packed as a wire message according to wire protocol
    """
    # Pack the header
    response = pack('!I', content.header)
    # Pack the Wire_Message payloads as appropriate according to wire protocol
    if content.header == CREATE_SUCCESS or content.header == CREATE_FAILURE:
        response += pack('!32s', content.payload['username'])
    if content.header == LOGIN_SUCCESS or content.header == LOGIN_FAILURE:
        response += pack('!32s', content.payload['username'])
    if content.header == ACCOUNT_LIST:
        # Pack the wildcard
        response += pack('!32s', content.payload['wildcard'])
        # First pack the number of users in the list being returned
        response += pack('!I', len(content.payload['accounts']))
        # Loop through each username in the list and pack it
        for user in content.payload['accounts']:
            response += pack('!32s', user)
    if content.header == DELETION_SUCCESS or content.header == DELETION_FAILURE:
        response += pack('!32s', content.payload['username'])
    if content.header == DISTRIBUTE_MESSAGE:
        response += pack('!32s', content.payload['username']) + pack('!100s', content.payload['message'])
    return response

def manage(connection, lock, session_id, model):
    """
    Process requests and responses from the client by unpacking message encoded by wire protocol into Wire_Message object to be interpreted by the Model
    :param connection: client connection from which to these requests are received
    :param lock: thread lock
    :param session_id: session id
    :param model: model of class Model_262 that handles server logic for data after being processed in this message
    """
    # Continuously listen for client requests and responses
    while True:
        try:
            received = connection.recv(1024)
        except:
            # Connection down
            thread.exit()

        if len(received) >= 4:
            # Unpack header
            header = unpack('!I', received[0:4])[0]
            payload = {}
            # Create payload of Wire_Message object according to header
            if header == CREATE_ACCOUNT:
                payload['username'] = unpack('!32s', received[4:])[0]
            elif header == LOGIN_REQUEST:
                payload['username'] = unpack('!32s', received[4:])[0]
            elif header == LIST_ACCOUNTS:
                payload['wildcard'] = unpack('!32s', received[4:])[0]
            elif header == SEND_MESSAGE:
                payload['from'] = unpack('!32s', received[4:36])[0]
                payload['to'] = unpack('!32s', received[36:68])[0]
                payload['message'] = unpack('!100s', received[68:])[0]
            elif header == DELETION_REQUEST:
                payload['username'] = unpack('!32s', received[4:36])[0]
                payload['forced'] = unpack('?', received[36:])[0]
            elif header == MESSAGE_RECEIPT:
                payload['username'] = unpack('!32s', received[4:36])[0]
                payload['from_user'] = 'Anon'
                payload['message'] = unpack('!100s', received[36:])[0]
                model.interpret(Wire_Message(header, payload), session_id)
            elif header == PULL_MESSAGES:
                try:
                    username = unpack('!32s', received[4:])[0]
                    messages = model.get_messages(username)
                    # Loop through all messages when pulling for a user
                    for m in messages:
                        h = DISTRIBUTE_MESSAGE
                        payload = {}
                        payload['username'] = username
                        payload['message'] = m
                        response = prep_response(Wire_Message(h, payload))
                        send_wire_message(connection, response)
                except:
                    continue
                continue
            else:
                print 'Unrecognized protocol operation'

            # Do not respond to MESSAGE_RECEIPT
            if header != MESSAGE_RECEIPT:
                # Send appropriate response after processing of request by Model and correctly packing response by prep_response
                response = prep_response(model.interpret(Wire_Message(header, payload), session_id))
                send_wire_message(connection, response)

class Controller():
    """
    Server Controller class
    :param host: the host to run the server
    :param port: the port to run the server
    
    Creates the server socket, and continually handles connections and wire
    messages adhering to the protocol. 
    """

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

            # Allocate new thread to independently and continuously listen to 
            # each connected client
            lock = thread.allocate_lock()
            thread.start_new_thread(manage, (clientsocket, lock, counter, self.model))
            print 'Connected with ' + address[0] + ':' + str(address[1])
            counter += 1

        self.server_socket.close()
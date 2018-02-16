from client_send import *
import socket
import os
import sys

logged_in = False

# Create socket and attempt connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

response_headers = {  CREATE_SUCCESS: create_success,
                    CREATE_FAILURE: create_failure,
                    LOGIN_SUCCESS: login_success,
                    LOGIN_FAILURE: login_failure,
                    ACCOUNT_LIST: out_list_accounts,
                    MESSAGE_SUCCESS: message_success,
                    MESSAGE_FAILURE: message_failure,
                    MESSAGE_PENDING: message_pending,
                    DELETION_SUCCESS: deletion_success,
                    DELETION_FAILURE: deletion_failure
           }

def exit_program():
    """
    Exiting the program involves closing connection and outputting good bye message
    """
    client_socket.close()
    print 'Thank you for using chat. Good bye.'
    sys.exit()

def prompt_user():
    """
    Primary control logic
    Taking user input and calling appropriate function
    """
    # User must first login or create account
    if not logged_in:
        print '''
        ***************
        Welcome to Chat.
        You are not logged in.
        Enter a number corresponding to any of the following options:
            1 - LOGIN
            2 - CREATE ACCOUNT
            3 - LIST ACCOUNTS
            0 - EXIT
        '''
        # Take input
        option = raw_input('Select an option: ')
        os.system('clear')  
        option_num = -1
        try:
            option_num = int(option)
        except:
            print 'Please enter a single number corresponding to one of the available options'
            return

        # Handle various options
        if option_num == 1:
            login(client_socket)
            return
        if option_num == 2:
            create_account(client_socket)
            return
        if option_num == 3:
            get_list_accounts(client_socket)
            return
        if option_num == 0:
            exit_program()
        print 'Please enter a single number corresponding to one of the available options'
        return

    # If logged in, choose one of these options
    print '''
        Welcome to Chat.
        Select one of the following options:
            1 - SEND MESSAGE
            2 - DELETE ACCOUNT
            3 - LIST ACCOUNTS
            0 - Exit
    '''
    # Take input
    option = raw_input('Select an option: ')
    os.system('clear')
    option_num = -1
    try:
        option_num = int(option)
    except:
        print 'Please enter a single number corresponding to one of the available options'
        return

    # Handle various options
    if option_num == 1:
        send_message(client_socket)
        return
    if option_num == 2:
        delete_account(client_socket)
        return
    if option_num == 3:
        get_list_accounts(client_socket)
        return
    if option_num == 0:
        exit_program(client_socket)
    print 'Please enter a single number corresponding to one of the available options'
    return

def get_response():
    """
    Keep listening for server response
    """
    try:
        received = client_socket.recv(1024)
    except:
        print 'Unable to send message; connection closed'
        sys.exit()
    header = unpack('!I', received[0:4])[0]
    response_headers[header](received)

def listen(lock):
    """
    Separate thread for clients to continuously listen for incoming messages
    """
    while True:
        try:
            received = conn.recv(1024)
        except:
            # Exit if no connection
            thread.exit()

        if len(netbuffer) >= 4:
            # Only receive messages
            header = received.unpack('!I', received[0:4])
            if header != DISTRIBUTE_MESSAGE:
                continue
            else:
                sender = received.unpack('!32s', received[4:36])
                content = received.unpack('!100s', received[36:])
                print('[MESSAGE FROM ' + sender + ']: ' + content)
                receipt_msg = pack('!I', MESSAGE_RECEIPT);
                send_wire_message(client_socket, receipt_msg)

def init():
    """
    Connecting the client to the server
    """
    # Require parameters for host and port
    if len(sys.argv) != 3:
        print 'Error. Usage: python2.7 client.py <host> <port>'
        sys.exit()
    host = sys.argv[1]
    port = sys.argv[2]

    try:
        client_socket.connect((host, int(port)))
    except socket.error as err:
        print 'Error connecting to server at ' + host + ':' + port + ': ' + str(err)
        sys.exit()
    print 'Successfully connected to server at ' + host + ':' + port

    # Start a new thread to continuously listen for incoming messages
    # lock = thread.allocate_lock()
    # thread.start_new_thread(listen, (lock))

    # Loop
    while True:
        prompt_user()
        get_response()

if __name__ == '__main__':
    init()

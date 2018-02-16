from client_send import *
import socket
import os
import sys
import time

logged_in = False
logged_in_user = None

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
                    DELETION_FAILURE: deletion_failure,
                    DISTRIBUTE_MESSAGE: message_received
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
    valid = False
    time.sleep(1)
    while not valid:
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
                continue

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
            continue
            return

        # If logged in, choose one of these options
        print ''
        print '        ***************'
        print '        Welcome ' + logged_in_user
        print'''        Select one of the following options:
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
            continue
            return

        # Handle various options
        if option_num == 1:
            send_message(client_socket, logged_in_user)
            return
        if option_num == 2:
            delete_account(client_socket, logged_in_user)
            return
        if option_num == 3:
            get_list_accounts(client_socket)
            return
        if option_num == 0:
            exit_program()
        print 'Please enter a single number corresponding to one of the available options'
        continue
    return

def listen(lock, connection):
    """
    Separate thread for clients to continuously listen for incoming messages and responses
    """
    while True:
        try:
            received = connection.recv(1024)
        except:
            print 'Unable to send message; connection closed'
            sys.exit()

        if len(received) >= 4:
            # Only receive messages
            global logged_in
            global logged_in_user
            header = unpack('!I', received[0:4])[0]
            if header == LOGIN_SUCCESS:
                logged_in = True
                logged_in_user = unpack('!32s', received[4:])[0]
            if header == DELETION_SUCCESS:
                logged_in = False
                logged_in_user = None
            if header == DISTRIBUTE_MESSAGE:
                receipt_msg = pack('!I', MESSAGE_RECEIPT) + received[4:]
                try:
                    connection.send(receipt_msg)
                except:
                    print 'Unable to send message; connection closed'
                    sys.exit()
            response_headers[header](received)

def pull(lock, connection):
    while True:
        time.sleep(0.5)
        if logged_in_user != None:
            try:
                connection.send(pack('!I', PULL_MESSAGES) + pack('!32s', logged_in_user))
            except:
                pass

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

    os.system('clear')

    # Start a new thread to continuously listen for incoming messages and responses
    lock = thread.allocate_lock()
    thread.start_new_thread(listen, (lock, client_socket))

    lock2 = thread.allocate_lock()
    thread.start_new_thread(pull, (lock2, client_socket))
    # Loop
    while True:
        prompt_user()

if __name__ == '__main__':
    init()

from client_send import *
import socket
import sys

logged_in = False

# Create socket and attempt connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        print '\n'
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
            list_accounts(client_socket)
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
    print '\n'
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
        list_accounts(client_socket)
        return
    if option_num == 0:
        exit_program(client_socket)
    print 'Please enter a single number corresponding to one of the available options'
    return

def listen():
    while True:
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

    # Loop
    while True:
        prompt_user()
        listen()

if __name__ == '__main__':
    init()

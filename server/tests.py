from Model import Model_262
from Wire_Message import Wire_Message
from protocol_strings import *

def test_creation():
    model = Model_262()
    payload = {}
    payload["username"] = 'user1'
    ret = model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    assert(ret.header == CREATE_SUCCESS)
    assert(model.data.usernames['user1'] == True)
    assert(model.data.active_sessions.has_key('user1') == False)
    
    ret = model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    assert(ret.header == CREATE_FAILURE)
    
    print "Account Creation OK"


def test_login():
    model = Model_262()
    payload = {}
    payload["username"] = 'user1'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    
    ret = model.interpret(Wire_Message(LOGIN_REQUEST, payload), 123)
    assert(ret.header == LOGIN_SUCCESS)
    assert(model.data.active_sessions['user1'] == 123)
    
    payload["username"] = 'nope_user'
    ret = model.interpret(Wire_Message(LOGIN_REQUEST, payload), 123)
    assert(ret.header == LOGIN_FAILURE)
    
    print "Login OK"


def test_list_accounts():
    model = Model_262()
    payload1 = {}
    payload1["username"] = 'user1'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload1), -1)

    payload2 = {}
    payload2["username"] = 'user2'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload2), -1)
    
    payload3 = {}
    payload3["wildcard"] = ''
    ret = model.interpret(Wire_Message(LIST_ACCOUNTS, payload3), -1)
    assert(ret.header == ACCOUNT_LIST)
    assert(ret.payload["accounts"] == ['user1', 'user2'] or 
           ret.payload["accounts"] == ['user2', 'user1'])
    
    payload3 = {}
    payload3["wildcard"] = '^u.*2$'
    ret = model.interpret(Wire_Message(LIST_ACCOUNTS, payload3), -1)
    assert(ret.header == ACCOUNT_LIST)
    assert(ret.payload["accounts"] == ['user2'])
    assert(ret.payload["wildcard"] == '^u.*2$')
    
    print "Account Listing OK"
    
    


def test_messaging():
    model = Model_262()
    payload1 = {}
    payload1["username"] = 'user1'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload1), -1)
    model.interpret(Wire_Message(LOGIN_REQUEST, payload1), 123)
    
    payload2 = {}
    payload2["username"] = 'user2'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload2), -1)
    #model.interpret(Wire_Message(LOGIN_REQUEST, payload2), 123)
    # account exists but isn't logged in
    
    # send a message from user1 to user2
    payload1["from"] = 'user1'
    payload1["to"] = 'user2'
    payload1["message"] = "hello"
    ret = model.interpret(Wire_Message(SEND_MESSAGE, payload1), 123)
    assert(ret.header == MESSAGE_PENDING)
    assert(model.data.pending_messages['user2'] == ["hello"])
    
    payload1["message"] = "hello2"
    model.interpret(Wire_Message(SEND_MESSAGE, payload1), 123)
    assert(model.data.pending_messages['user2'] == ["hello", "hello2"])
    
    
    # message distribution ticks
    ret = model.get_pending_messages()
    assert(ret[0].header == DISTRIBUTE_MESSAGE)
    assert(ret[0].payload["message"] == "hello")
    assert(ret[1].payload["message"] == "hello2")
    
    
    # test message failure
    payload1["message"] = "hello2"
    payload1["to"] = 'nope_user'
    ret = model.interpret(Wire_Message(SEND_MESSAGE, payload1), 123)
    assert(ret.header == MESSAGE_FAILURE)
    assert(model.data.pending_messages['user2'] == ["hello", "hello2"])
    
    
    # simulate client confirmation of receipt
    payload3 = {}
    payload3["username"] = 'user2'
    payload3["message"] = "hello"
    payload3["from_user"] = 'user1'
    model.interpret(Wire_Message(MESSAGE_RECEIPT, payload3), -1)
    
    ret = model.get_pending_messages()
    assert(ret[0].payload["message"] == "hello2")
    assert(len(ret) == 1)
    
    print "Messaging OK"


def test_deletion():
    # creation
    model = Model_262()
    payload = {}
    payload["username"] = 'user1'
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    
    # test proper deletion failure
    model.data.pending_messages['user1'] = ["some_message"]
    ret = model.interpret(Wire_Message(DELETION_REQUEST, payload), -1)
    assert(ret.header == DELETION_FAILURE)
    
    # test force deletion
    payload["forced"] = True
    ret = model.interpret(Wire_Message(DELETION_REQUEST, payload), -1)
    assert(ret.header == DELETION_SUCCESS)
    assert(model.data.usernames['user1'] == None)
    assert(model.data.pending_messages['user1'] == None)
    assert(model.data.active_sessions['user1'] == None)
    print "Account Deletion OK"


print "\nTesting...\n"
test_creation()
test_login()
test_list_accounts()
test_messaging()
test_deletion()
print "Testing complete\n"




# Tested:
# o  CREATE_ACCOUNT
# o  CREATE_SUCCESS
# o  CREATE_FAILURE
# o  LOGIN_REQUEST 
# o  LOGIN_SUCCESS 
# o  LOGIN_FAILURE 
# o  LIST_ACCOUNTS     
# o  ACCOUNT_LIST      
# o  SEND_MESSAGE      
# o  MESSAGE_SUCCESS   
# o  MESSAGE_FAILURE   
# o  MESSAGE_PENDING            
# o  DISTRIBUTE_MESSAGE
# o  MESSAGE_RECEIPT
# o  DELETION_REQUEST
# o  DELETION_SUCCESS
# o  DELETION_FAILURE

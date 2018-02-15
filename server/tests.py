from Model import Model_262
from Wire_Message import Wire_Message
from protocol_strings import *

def test_creation():
    model = Model_262()
    payload = {}
    payload["username"] = "user1"
    ret = model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    assert(ret.header == CREATE_SUCCESS)
    assert(model.data.usernames["user1"] == True)
    assert(model.data.active_sessions.has_key("user1") == False)
    print "Account Creation OK"


def test_login():
    model = Model_262()
    payload = {}
    payload["username"] = "user1"
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    
    ret = model.interpret(Wire_Message(LOGIN_REQUEST, payload), 123)
    assert(ret.header == LOGIN_SUCCESS)
    assert(model.data.active_sessions["user1"] == 123)
    
    # TODO test login collision
    
    print "Login OK"


def test_messaging():
    model = Model_262()
    payload1 = {}
    payload1["username"] = "user1"
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload1), -1)
    model.interpret(Wire_Message(LOGIN_REQUEST, payload1), 123)
    
    payload2 = {}
    payload2["username"] = "user2"
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload2), -1)
    #model.interpret(Wire_Message(LOGIN_REQUEST, payload2), 123)
    # account exists but isn't logged in
    
    # send a message from user1 to user2
    payload1["from"] = "user1"
    payload1["to"] = "user2"
    payload1["message"] = "hello"
    ret = model.interpret(Wire_Message(SEND_MESSAGE, payload1), 123)
    assert(ret.header == MESSAGE_PENDING)
    assert(model.data.pending_messages["user2"] == ["hello"])
    
    payload1["message"] = "hello2"
    model.interpret(Wire_Message(SEND_MESSAGE, payload1), 123)
    assert(model.data.pending_messages["user2"] == ["hello", "hello2"])
    
    
    # message distribution ticks
    ret = model.get_pending_messages()
    assert(ret[0].header == DISTRIBUTE_MESSAGE)
    assert(ret[0].payload["message"] == "hello")
    assert(ret[1].payload["message"] == "hello2")
    
    
    # simulate client confirmation of receipt
    payload3 = {}
    payload3["username"] = "user2"
    payload3["message"] = "hello"
    payload3["from_user"] = "user1"
    model.interpret(Wire_Message(MESSAGE_RECEIPT, payload3), -1)
    
    ret = model.get_pending_messages()
    assert(ret[0].payload["message"] == "hello2")
    assert(len(ret) == 1)
    
    print "Messaging OK"


def test_deletion():
    # creation
    model = Model_262()
    payload = {}
    payload["username"] = "user1"
    model.interpret(Wire_Message(CREATE_ACCOUNT, payload), -1)
    
    # TODO test w/out forced
    
    # deletion
    payload["forced"] = False
    ret = model.interpret(Wire_Message(DELETION_REQUEST, payload), -1)
    assert(ret.header == DELETION_SUCCESS)
    assert(model.data.usernames["user1"] == None)
    assert(model.data.pending_messages["user1"] == None)
    assert(model.data.active_sessions["user1"] == None)
    print "Account Deletion OK"


print "\nTesting...\n"
test_creation()
test_login()
test_messaging()
test_deletion()
print "Testing complete\n"


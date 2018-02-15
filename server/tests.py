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

def test_message():
    # TODO
    pass

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



test_creation()
test_login()
test_message()
test_deletion()


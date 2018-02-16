# Note: no native Enums, and don't want to complicate install

# HEADERS
CREATE_ACCOUNT              = 0x00001
CREATE_SUCCESS              = 0x00010
CREATE_FAILURE              = 0x01101 # added
LOGIN_REQUEST               = 0x00011
LOGIN_SUCCESS               = 0x00100
LOGIN_FAILURE               = 0x01111 # added
LIST_ACCOUNTS               = 0x00101
ACCOUNT_LIST                = 0x00110
SEND_MESSAGE                = 0x00111
MESSAGE_SUCCESS             = 0x01000
MESSAGE_FAILURE             = 0x10000 # added
MESSAGE_PENDING             = 0x10001 # added
DISTRIBUTE_MESSAGE          = 0x01001
MESSAGE_RECEIPT             = 0x01010
DELETION_REQUEST            = 0x01011
DELETION_SUCCESS            = 0x01100
DELETION_FAILURE            = 0x10010 # added
PULL_MESSAGES               = 0x10100 # added

'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

from struct import pack
import protocol


# General failure is a method used to send any failure message, tagged with a typebyte associated with a particular operation
def general_failure(conn, type, reason):

    # Find the appropriate opcode to send for particular errors
    msg_type = None
    if type == 'create':
        msg_type = protocol.CreateFailResponse
    elif type == 'delete':
        msg_type = protocol.DeleteFailResponse
    elif type == 'login':
        msg_type = protocol.LoginFailResponse
    elif type == 'logout':
        msg_type = protocol.LogoutFailResponse
    elif type == 'send_message':
        msg_type = protocol.SendFailResponse
    elif type == 'collect_messages':
        msg_type = protocol.CollectFailResponse
    else:
        raise ValueError("Type {} is not a valid failure type.".format(type))

    conn.send(protocol.make_message(msg_type, reason))
    return


# Create new account success
# The account is created and the client is logged in to that account
def create_success(conn):
    conn.send(protocol.make_message(protocol.CreateSuccessResponse))


# Delete an existing account success
# The client will be logged out of the account, and account deleted
def delete_success(conn):
    conn.send(protocol.make_message(protocol.DeleteSuccessResponse))


# Login success
# The client is logged in
def login_success(conn):
    conn.send(protocol.make_message(protocol.LoginSuccessResponse))


# Logout success
# The client is logged out
def logout_success(conn):
    conn.send(protocol.make_message(protocol.LogoutSuccessResponse))


# Send message success
# Returns whether the messages were undelivered and stored or delivered immediately
def send_message_success(conn, received):
    # If received is true, the destination user was active
    # Else, the user's messages are collected in the server
    # received is a boolean - do we want to send it as such? is it worth even notifying the client of this?

    if received:
        msg = 'Destination user is online; messages delivered'
        msg_type = protocol.SendSuccessResponse
    else:
        msg = 'Destination user is not online; messages will be delivered later'
        msg_type = protocol.SendQueuedResponse

    msg_binary = protocol.make_message(msg_type, msg)

    conn.send(msg_binary)

# Collect message success
# Returns a list of messages that were previously undelivered
def collect_messages_success(conn, messages):
    # What happens in the case of partial failure to send a message?
    if len(messages) == 0:
        conn.send(b'\x01\x00\x00\x00\x00\x63')
    for message in messages:
        utf = message.encode('utf-8')
        utflen = len(utf)
        conn.send(b'\x01' + pack('!I',2 + utflen) + b'\x61' + pack('!h',utflen) + utf)
    return

# Handle invalid opcodes
def unknown_opcode(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x71')
    return

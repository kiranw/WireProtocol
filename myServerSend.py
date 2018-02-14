'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

from struct import pack


# General failure is a method used to send any failure message, tagged with a typebyte associated with a particular operation
def general_failure(conn, type, reason):
    
    # Find the appropriate opcode to send for particular errors
    if type == 'create':
        typebyte = b'\x12'
    elif type == 'delete':
        typebyte = b'\x22'
    elif type == 'login':
        typebyte = b'\x32'
    elif type == 'logout':
        typebyte = b'\x42'
    elif type == 'send_message':
        typebyte = b'\x52'
    elif type == 'collect_messages':
        typebyte = b'\x62'
    
    # Encode and send the string
    utf = reason.encode('utf-8')
    utflen = len(utf)
    conn.send(b'\x01' + pack('!I',2 + utflen) + typebyte + pack('!h',utflen) + utf)
    return


# Create new account success
# The account is created and the client is logged in to that account
def create_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x11')
    return


# Delete an existing account success
# The client will be logged out of the account, and account deleted
def delete_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x21')
    return


# Login success
# The client is logged in
def login_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x31')
    return

# Logout success
# The client is logged out
def logout_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x41')
    return


# Send message success
# Returns whether the messages were undelivered and stored or delivered immediately
def send_message_success(conn,received):
    # If received is true, the destination user was active
    # Else, the user's messages are collected in the server
    # received is a boolean - do we want to send it as such? is it worth even notifying the client of this?
    msg = 'Destination user is not online; messages will be delivered later'
    if received:
        msg = 'Destination user is online; messages delivered'

    utf = msg.encode('utf-8')
    utflen = len(utf)
    conn.send(b'\x01' + pack('!I',2 + utflen) + b'\x51' + pack('!h',utflen) + utf)
    return

# Collect message success
# Returns a list of messages that were previously undelivered
def collect_messages_success(conn, messages):
    # What happens in the case of partial failure to send a message?
    if len(messages) == 0:
        conn.send(b'\x01\x00\x00\x00\x00\x72')
    for message in messages:
        utf = message.encode('utf-8')
        utflen = len(utf)
        conn.send(b'\x01' + pack('!I',2 + utflen) + b'\x61' + pack('!h',utflen) + utf)
    return

# Handle invalid opcodes
def unknown_opcode(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x71')
    return



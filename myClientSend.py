'''
Created on Feb 18, 2010
altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit





# Create new account
# A user submits an account name (must be less than 100 characters)
# If account creation is successful, the user will automatically be
# logged in to their account (create_success, \x11)
# On failure, a failure message is received (general_failure, \x12)
# 
# Arguments sent to server:
# act - account name
def create_request(conn):
    print("CREATING AN ACCOUNT \n")
    print("Enter a username less than 100 characters:")
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        elif(netBuffer == 0):
            act = -1
            break

    send_message('\x01' + pack('!I',100) + '\x10' + pack('!100p',act),conn)
    
    return


# Delete the account that is currently logged in
# A user will be logged out and the account deleted if this request
# is successful (delete_success, \x21)
# On failure, a failure message is received (general_failure, \x22)
def delete_request(conn):
    print("DELETING YOUR ACCOUNT \n")    
    send_message('\x01\x00\x00\x00\x00\x20',conn)
    return


# Login to an existing account
# A user will submit a username
# On success, the user will be logged in (login_success, \x31)
# on failure, the user will remain logged out (general_failure, \x32)
# 
# Arguments sent to server:
# act - account name
def login_request(conn):
    print("LOGGING YOU IN \n")
    print("Enter your username:")
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        
    send_message('\x01' + pack('!I',100) + '\x30' + pack('!100p',act),conn)
    return


# Logout of an account that is currently logged in
# On success, the user will be logged out (logout_success, \x41)
# on failure, the user will remain logged in, or logged out if that was
# their previous state (general_failure, \x42)
def logout_request(conn):
    print("LOGGING YOU OUT \n")        
    send_message('\x01\x00\x00\x00\x00\x40',conn)
    return


# Send a message to an existing account
# On success, the server receives the message from the user (send_message_success, \x51)
# This does not mean the destination account has received the message
# On failure, the message is not received by the server (general_failure, \x52)
# 
# Arguments sent to server:
# dest_act - destination account
# msg - message content
def send_message_request(conn):
    print("SEND A MESSAGE TO ANOTHER USER \n")
    print("Enter the destination account name:")
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            dest_act = netBuffer
            break

    print("Enter your message:")
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            msg = netBuffer
            break

    send_message('\x01' + pack('!I',400) + '\x50' + pack('!100p300p',dest_act,msg),conn)
    return


# Collect undelivered messages
# On success, the user receives any messages that were previously undelivered (collect_messages_success, \x61)
# On failure, the user does not receive undelievered messages, if they exist (general_failure, \x62)
def collect_messages_request(conn):
    send_message('\x01\x00\x00\x00\x00\x60',conn)
    return


# Sends a message from the client to the server using the connection provided.
# message - A message contains the following information:
# (1) version number
# (2) argument length
# (3) operation code
# (4) arguments
# conn - A connection to the server
# On failure (if the connection is down) the client closes
def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print("ERROR: connection down")
            exit()
    return

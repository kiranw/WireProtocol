'''
Created on Feb 18, 2010
Altered Feb. 20, 2014

Adapted by Mali and Kiran for Assignment 1, CS262
'''

from struct import unpack
from sys import exit

# Handle errors from server side. This method is a generic method that returns any specific
# error it receives from the server.
def general_failure(conn, netBuffer):
    values = unpack('!h',netBuffer[6:8])
    strlen = values[0]
    print("\nERROR: " + netBuffer[8:8+strlen].decode('ascii'))
    return


# Create a new account
# If account creation is successful, the user will automatically be
# logged in to their account (create_success, \x11)
def create_success(conn, netBuffer):
    print("Account creation successful - you are currently logged in.")
    return


# Delete the account that is currently logged in
# A user will be logged out and the account deleted if this request
# is successful (delete_success, \x21)
def delete_success(conn, netBuffer):
    print("Account deletion successful")
    return


# Login to an existing account
# On success, the user will be logged in (login_success, \x31)
def login_success(conn,netBuffer):
    print("Login success! You are logged in.")
    return


# Logout of an account that is currently logged in
# On success, the user will be logged out (logout_success, \x41)
def logout_success(conn,netBuffer):
    print("Logout success! You are logged out. Disconnecting from server.")
    conn.close()
    exit()
    return


# Send a message to an existing account
# On success, the server receives the message from the user (send_message_success, \x51)
# This does not mean the destination account has received the message 
# (if the destination user is not logged in when the message is received by the server)
def send_message_success(conn,netBuffer):
    print("Messages sent successfully! Your messages were received by the server.")
    return


# Collect undelivered messages
# On success, the user receives any messages that were previously undelivered (collect_messages_success, \x61)
# Each message is printed for the user
def collect_messages_success(conn,netBuffer):
    # TODO - needs to be figured out for what is returned here
    values = unpack('!h',netBuffer[6:8])
    strlen = values[0]
    for i in range(strlen):
        print("Message " + i)
        print("Received from " + i)
        print("message: " + i)
        print("\n")
    return

# Handle invalid opcodes received from the server.
def unknown_opcode(conn):
    print("ERROR: INCORRECT OPCODE")
    return
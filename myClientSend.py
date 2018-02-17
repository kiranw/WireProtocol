'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

import protocol
from util import printGreen, printRed


# Create new account
# A user submits an account name (must be less than 100 characters)
# If account creation is successful, the user will automatically be
# logged in to their account (create_success, \x11)
# On failure, a failure message is received (general_failure, \x12)
#
# Arguments sent to server:
# act - account name
def create_request(conn):
    maxLength = 100

    printGreen("CREATING AN ACCOUNT")
    printGreen("Enter a username less than 100 characters:")

    account_name = ""
    while True:
        account_name = input()

        if(len(account_name) < maxLength):
            send_message(protocol.make_message(protocol.CreateRequest, account_name), conn)
            return
        else:
            printRed("Exceeded length of username, must be less than 100 characters")


# Delete the account that is currently logged in
# A user will be logged out and the account deleted if this request
# is successful (delete_success, \x21)
# On failure, a failure message is received (general_failure, \x22)
def delete_request(conn):
    printGreen("DELETING YOUR ACCOUNT")
    send_message(protocol.make_message(protocol.DeleteRequest), conn)
    return


# Login to an existing account
# A user will submit a username
# On success, the user will be logged in (login_success, \x31)
# on failure, the user will remain logged out (general_failure, \x32)
#
# Arguments sent to server:
# act - account name
def login_request(conn):
    maxLength = 100
    printGreen("LOGGING YOU IN")
    printGreen("Enter your username:")
    while True:
        account_name = input()

        if(len(account_name) < maxLength):
            send_message(protocol.make_message(protocol.LoginRequest, account_name), conn)
            return
    return


# Logout of an account that is currently logged in
# On success, the user will be logged out (logout_success, \x41)
# on failure, the user will remain logged in, or logged out if that was
# their previous state (general_failure, \x42)
def logout_request(conn):
    printGreen("LOGGING YOU OUT")
    send_message(protocol.make_message(protocol.LogoutRequest), conn)
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
    printGreen("SEND A MESSAGE TO ANOTHER USER")
    printGreen("Enter the destination account name:")
    while True:
        dest_account = input('>> ')
        if (len(dest_account) < 100):
            break

    printGreen("Enter your message:")
    while True:
        message = input('>> ')
        if(len(message) < 255):
            break

    send_message(protocol.make_message(protocol.SendMessageRequest, dest_account, message), conn)
    return


# Collect undelivered messages
# On success, the user receives any messages that were previously undelivered (collect_messages_success, \x61)
# On failure, the user does not receive undelievered messages, if they exist (general_failure, \x62)
def collect_messages_request(conn):
    send_message(protocol.make_message(protocol.CollectMessageRequest), conn)
    return

# Checks if message collection is complete
# On success,
#   if there are no new messages, server responds confirming there are no new messages
#   server returns with a new message if there is one    
# On failure, the user does not receive undelievered messages, if they exist (general_failure, \x62)
def confirm_collection_complete_request(conn):
    send_message(protocol.make_message(protocol.ConfirmCollectMessageRequest), conn)
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
        # Close the client if the connection is down
        printRed("ERROR: Oh no! It looks like the connection is down. Try again some other time!")
        exit()
    return

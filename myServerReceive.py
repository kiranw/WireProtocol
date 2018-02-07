'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

from myServerSend import *
from struct import unpack
import sys

# Create a new account
# A valid new account must not exist
# A user can only create an account if they are not logged in
# Once an account is created, the client will be logged in
# act - the account name provided by the user
def create_request(conn,netBuffer,myData,lock,address):
    print(len(netBuffer))
    values = unpack('!100p',netBuffer[6:107])

    lock.acquire()
    try:
        if address in myData['active_accounts']:
            general_failure(conn,'create',"User is currently logged in. Cannot create a new account.")
            return

        if values[0]:
            act = values[0].decode('ascii')
            if act in myData['accounts']:
                general_failure(conn,'create',"Account already in use; select a different username")
                return

        myData['accounts'].append(act)
        myData['active_accounts'][address] = act
        print("Added account, " + act)
        create_success(conn)
    finally:
        lock.release()
        print(myData)
    return

# Delete the account that is currently logged in
# A user will be logged out and the account deleted if this request
# is successful (delete_success, \x21)
# On failure, a failure message is received (general_failure, \x22)
def delete_request(conn,netBuffer,myData,lock,address):
    # values = unpack('!I',netBuffer[6:10])

    lock.acquire()
    try:
        # Check if the current user is logged in
        if address not in myData['active_accounts']:
            general_failure(conn,'delete',"User is not logged in; Cannot delete account")
            return

        act = myData['active_accounts'][address]
        myData['accounts'].remove(act)
        del myData['active_accounts'][address]
        delete_success(conn)
    finally:
        lock.release()
        print(myData)
    return


# Login to an existing account
# A user will submit a username
# On success, the user will be logged in (login_success, \x31)
# on failure, the user will remain logged out (general_failure, \x32)
# 
# Arguments sent to server:
# act - account name
def login_request(conn,netBuffer,myData,lock,address):
    values = unpack('!100p',netBuffer[6:106])
    lock.acquire()
    try:
        if values[0]:
            act = values[0].decode('ascii')

            # See if this user is logged in already
            if address in myData['active_accounts']:
                general_failure(conn,'login',"User is currently logged in to an account. Cannot login.")
                return

            # See if account name exists
            if act not in myData['accounts']:
                general_failure(conn,'login',"Account does not exist. Cannot login.")
                return

            # See if account is already logged in
            if act in myData['active_accounts']:
                general_failure(conn,'login',"Account is already logged in to another user.")
                return

            # Mark user as active
            myData['active_accounts'][address] = act
            login_success(conn)
    finally:
        lock.release()
        print(myData)
    return


# Logout of an account that is currently logged in
# On success, the user will be logged out (logout_success, \x41)
# on failure, the user will remain logged in, or logged out if that was
# their previous state (general_failure, \x42)
def logout_request(conn,netBuffer,myData,lock,address):
    values = unpack('!100p',netBuffer[6:106])
    lock.acquire()
    try:
        if values[0]:
            act = values[0].decode('ascii')

            # See if this user is not logged in to anything
            if address not in myData['active_accounts']:
                general_failure(conn, 'logout',"User is already logged out.")
                return

            # Mark user as active
            myData['active_accounts'].remove(address)
            logout_success(conn)
    finally:
        lock.release()
        print(myData)
    return


# Send a message to an existing account
# On success, the server receives the message from the user (send_message_success, \x51)
# This does not mean the destination account has received the message
# On failure, the message is not received by the server (general_failure, \x52)
# 
# Arguments sent to server:
# dest_act - destination account
# msg - message content
def send_message_request(conn,netBuffer,myData,lock,address):
    values = unpack('!400p',netBuffer[6:106])
    dest_act = values[0].decode('ascii')
    msg = values[1].decode('ascii')

    lock.acquire()
    # Check if destination account is valid
    if dest_act not in myData['accounts']:
        general_failure(conn,'send_message',"Destination account does not exist.")
        return

    # Handle the message
    try:
        active_dest = False

        if dest_act in myData['active_accounts'].values():
            dest_address = dict((active_act, active_address) for active_address, active_account in myData['active_accounts'].iteritems())[dest_act]
            # That line is temporary, we should have to regenerate this each time
            # TODO send messages to active user, identify what thread that user is on (does each message get a from: field?)
            # Do threads need to poll some sort of list of pending messages to see if they should deliver?
            active_dest = True
            pass

        else:
            if dest_act not in myData['messages']:
                myData['messages'][dest_act] = []
            myData['messages'][dest_act].append(msg)
        
        send_message_success(conn, active_dest)
    finally:
        lock.release()
        print(myData)
    return


# Collect undelivered messages
# On success, the user receives any messages that were previously undelivered (collect_messages_success, \x61)
# On failure, the user does not receive undelievered messages, if they exist (general_failure, \x62)
def collect_messages(conn,netBuffer,myData,lock,address):
    lock.acquire()
    try:
        if address not in myData['active_accounts']:
            general_failure(conn,'collect_messages',"Current user is not logged in to an account.")
            return

        # Get the account name that is logged in at current address
        act = myData['active_accounts'][address]
        messages = []

        if act in myData['messages']:
            messages = myData['messages'][act]
        collect_messages_success(conn,messages)
    finally:
        lock.release()
        print(myData)
    return

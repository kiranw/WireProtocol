'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

import sys
import protocol


# Handle errors from server side. This method is a generic method that returns any specific
# error it receives from the server.
def general_failure(text):
    print("\nERROR: " + text)
    return


# Create a new account
# If account creation is successful, the user will automatically be
# logged in to their account (create_success, \x11)
def create_success():
    print("Account creation successful - you are currently logged in.")
    return


# Delete the account that is currently logged in
# A user will be logged out and the account deleted if this request
# is successful (delete_success, \x21)
def delete_success():
    print("Account deletion successful.")
    return


# Login to an existing account
# On success, the user will be logged in (login_success, \x31)
def login_success():
    print("Login success! You are logged in.")
    return


# Logout of an account that is currently logged in
# On success, the user will be logged out (logout_success, \x41)
def logout_success():
    print("Logout success! You are logged out.")
    return


# Send a message to an existing account
# On success, the server receives the message from the user (send_message_success, \x51)
# This does not mean the destination account has received the message
# (if the destination user is not logged in when the message is received by the server)
def send_message_success(response_text):
    print("\nMessages sent successfully: {}".format(response_text))
    return

# Send a message to an existing account
# On success, the message was queued because the destination user was not online
def send_queued_success(response_text):
    print("\nYour message was sent successfully, and is being queued")
    return

# Collect undelivered messages
# On success, the user receives any messages that were previously undelivered (collect_messages_success, \x61)
# Each message is printed for the user
def collect_messages_success(response_text):
    print("You received a message! Here: {}".format(response_text))
    return

def confirm_collection_success():
    return

def no_new_messages():
    print("You have no new messages.")
    return


def handle_list_users(user_list):
    user_list = user_list.split(";")

    if len(user_list) == 0:
        print("No matching users found.")
        return

    print("Matching users:")
    for user in user_list:
        print(user)

    return


# Handle invalid opcodes received from the server.
def unknown_opcode():
    print("ERROR: Invalid opcode received from server.")
    return


def end_session(message):
    print("Server ended the session: {}".format(message))
    sys.exit(0)
    return


response_handlers = {
    # Create_success
    protocol.CreateSuccessResponse: create_success,
    # Create failure
    protocol.CreateFailResponse: general_failure,
    # Delete success
    protocol.DeleteSuccessResponse: delete_success,
    # Delete failure
    protocol.DeleteFailResponse: general_failure,
    # Login success
    protocol.LoginSuccessResponse: login_success,
    # Login failure
    protocol.LoginFailResponse: general_failure,
    # Logout success
    protocol.LogoutSuccessResponse: logout_success,
    # Logout failure
    protocol.LogoutFailResponse: general_failure,
    # Send message success
    protocol.SendSuccessResponse: send_message_success,
    # Send message failure
    protocol.SendFailResponse: general_failure,
    # Send message queued
    protocol.SendQueuedResponse: send_queued_success,
    # Collect messages success
    protocol.CollectSuccessResponse: collect_messages_success,
    # Collect messages failure
    protocol.CollectFailResponse: general_failure,
    # No new messages
    protocol.CollectNoNewResponse: no_new_messages,
    # Confirm no new messages
    protocol.ConfirmCollectionCompleteResponse: confirm_collection_success,
    # User list based on wildcard
    protocol.ListUsersResponse: handle_list_users,

    # Server ended session
    protocol.EndSessionResponse: end_session,

    # Unknown opcode
    protocol.UnknownMessageResponse: unknown_opcode,
}

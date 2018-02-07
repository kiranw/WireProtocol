'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from struct import unpack
from sys import exit

#handle errors from server side.
def general_failure(conn, netBuffer):
    values = unpack('!h',netBuffer[6:8])
    strlen = values[0]
    print("\nERROR: " + netBuffer[8:8+strlen])
    return

# Create a new account. Users are automatically logged in once they create an account.
def create_success(conn, netBuffer):
    print("Account creation successful - you are currently logged in.")
    return

# Delete an existing account.
def delete_success(conn, netBuffer):
    print("Account deletion successful")
    return

# Log in to an account that already exists.
def login_success(conn,netBuffer):
    print("Login success! You are logged in.")
    return

# Logout of an account that is currently logged in.
def logout_success(conn,netBuffer):
    print("Logout success! You are logged out. Disconnecting from server.")
    conn.close()
    exit()
    return

# Send a message to a particular user.
def send_message_success(conn,netBuffer):
    print("Messages sent successfully! Your messages were received by the server.")
    return

# Receive undelivered messages to the account that is logged in.
def collect_messages_success(conn,netBuffer):
    # TODO - needs to be figured out for what is returned here
    values = unpack('!h',netBuffer[6:8])
    strlen = values[0]
    for i in range(strlen):
        print("Message " + i)
        print("Received from " + i)
        print("message: " + i)
    return

# Handle invalid opcodes.
def unknown_opcode(conn):
    print("ERROR: INCORRECT OPCODE")
    return
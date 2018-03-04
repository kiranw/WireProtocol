'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

import socket
import sys
import _thread as thread

import myClientSend
import myClientReceive
import protocol


# Print user menu and collect input to client
def user_menu():
    print('''
CONNECTED TO MESSAGE SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Login to Account
    (4) Logout
    (5) Send a Message
    (6) Check for Messages
    (7) List users
    ''')
    return input('>> ')


# Handle client request based on menu input
def run_submenu_selection(menu_number, mySocket):

    if menu_number == str(1):
        myClientSend.create_request(mySocket)

    #delete
    elif menu_number == str(2):
        myClientSend.delete_request(mySocket)

    #login
    elif menu_number == str(3):
        myClientSend.login_request(mySocket)

    #logout
    elif menu_number == str(4):
        myClientSend.logout_request(mySocket)

    #send a message to a user
    elif menu_number == str(5):
        myClientSend.send_message_request(mySocket)

    #collect undelivered messages
    elif menu_number == str(6):
        myClientSend.collect_messages_request(mySocket)

    #list users
    elif menu_number == str(7):
        myClientSend.list_users_request(mySocket)

    else:
        print("ERROR: Invalid menu option {}".format(menu_number))
        return False

    return True


# The current implementation for collecting undelivered messages responds with
# one message at a time. This method regenerates the request until there are
# no new messages
def handle_multiple_messages(mySocket):
    myClientSend.confirm_collection_complete_request(mySocket)
    getResponse(mySocket, "8", True)
    return

# Collect server response and handle using message type as specified in protocol
# If the response receieved does not match the response expected, getResponse again
# Makes sure client has collected all information from server until it is caught up to
# the current operation
# Menu number is used to check if responses correspond to requests made by the user
# If the response does not match, another response will be collected from the server until
# the client is caught up
def getResponse(mySocket, menu_number, discardResponse = False):
    while True:
        try:
            # Wait until I read a message
            message_type, message_args = protocol.receive_message(mySocket)

            # Dont relay to client if the message is terminating a cascade of collected messages
            if message_type == protocol.CollectNoNewResponse and discardResponse:
                return

            # Find the handler function for that message
            response_handler = myClientReceive.response_handlers.get(message_type, None)

            if response_handler is None:
                raise ValueError("There was no response handler found for message type {}".format(message_type))

            # Run the handler, passing in the stuff we decoded from the message
            response_handler(*message_args)

            # If the response doesn't match the request, we should get the next response after this operation finishes
            # Make sure client is caught up to the messages on the connection
            if protocol.matchingRequestResponse(menu_number, message_type):
                # If the client has not exhausted all messages, send another request to the server to pick up more
                if menu_number == "6" and message_type == protocol.CollectSuccessResponse:
                    handle_multiple_messages(mySocket)
                return

        except Exception:
            # close the client if the connection is down
            import traceback
            traceback.print_exc()
            print("ERROR: connection down")
            sys.exit()


if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print("ERROR: Usage 'python myClient.py <host> <port>'")
        sys.exit()

    #get the address of the server
    myHost = sys.argv[1]
    myPort = sys.argv[2]
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect ( ( myHost, int(myPort)) )

    except:
        print("ERROR: could not connect to " + myHost + ":" + myPort)
        sys.exit()

    while True:
        # Show user menu and return their selection
        menu_number = user_menu()

        # Run that submenu and send data
        run_submenu_selection(menu_number, mySocket)

        # Read corresponding response from server
        getResponse(mySocket, menu_number)

    mySocket.close()

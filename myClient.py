'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

import socket
from struct import unpack
import sys
import _thread as thread

import myClientSend
import myClientReceive
import protocol


def user_menu():
    print('''
CONNECTED TO MESSAGE SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Login to Account
    (4) Logout
    (5) Send a Message
    (6) Collect Undelivered Messages
    ''')
    return input('>> ')


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

    else:
        print("ERROR: Invalid menu option {}".format(menu_number))
        return False

    return True


def getResponse(mySocket, *args):
    while True:
        try:

            # Wait until I read a message
            message_type, message_args = protocol.receive_message(mySocket)
            print(message_type, message_args)

            # Find the handler function for that message
            response_handler = myClientReceive.response_handlers.get(message_type, None)

            if response_handler is None:
                raise ValueError("There was no response handler found for message type {}".format(message_type))

            # Run the handler, passing in the stuff we decoded from the message
            response_handler(*message_args)

        except Exception:
            # close the client if the connection is down
            import traceback
            traceback.print_exc()
            print("ERROR: connection down")
            sys.exit()

        return


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
        # listenerThread(mySocket).start()
    except:
        print("ERROR: could not connect to " + myHost + ":" + myPort)
        sys.exit()

    while True:
        # need to pause the listener thread when the
        # thread.start_new_thread(getInput, (mySocket,1))
        # thread.start_new_thread(getResponse, (mySocket,1))

        # Show user menu and return their selection
        menu_number = user_menu()

        # Run that submenu and send data
        run_submenu_selection(menu_number, mySocket)

        # Read corresponding response from server
        getResponse(mySocket)

    mySocket.close()

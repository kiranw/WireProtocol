'''
CS 262: Distributed Systems
Created on Feb 18, 2010
------------------------------
Restructured and re-factored by Jim Waldo, 2/17/2014
Adapted by Mali and Kiran for Assignment 1, CS262
'''

import logging
from logging.config import dictConfig
import socket
import struct
import sys
import _thread as thread
import traceback

import protocol
import myServerReceive
import myServerSend


# TODO
# Think about design of the collect messages function
# When connection is closed on client side, that is not reported to the server


logging_config = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root={
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

dictConfig(logging_config)

#thread for handling clients
def handler(conn, lock, myData, address):

    while True:
        print("trying")
        try:
            # Wait until I read a message
            message_type, message_args = protocol.receive_message(conn)
            logging.getLogger().info('Address %s: Received request %s: %s ', address, message_type, message_args)

            # Find the handler function for that message
            request_handler = myServerReceive.request_handlers.get(message_type, None)
            print("request handler:", request_handler)

            if request_handler is None:
                myServerSend.unknown_opcode(conn)
                raise ValueError("There was no response handler found for message type {}".format(message_type))

            # Run the handler, passing in the stuff we decoded from the message
            request_handler(conn, message_args, myData, lock, address)

            logging.getLogger().info('Server state: {}', myData)

        except:
            # Tell the client we're ending their session and log them out
            myServerSend.end_session(conn, "Server side exception, closing connection.")

            # Log out user
            if address in myData['active_accounts']:
                del myData['active_accounts'][address]
                del myData['connections'][address]

            conn.close()

            traceback.print_stack()
            traceback.print_exc()
            # close the thread if the connection is down
            thread.exit()


if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print("Invalid input, proper usage: 'python3 myServer.py <port>'")
        sys.exit()

    # Data structure for storing account information
    accounts = []

    # A list of messages is associated with a username
    messages = {}

    # Active accounts, maps addresses to accounts
    active_accounts = {}

    # Connections, maps addresses to connections
    connections = {}

    myData = {
    'accounts': accounts,
    'messages': messages,
    'active_accounts': active_accounts,
    'connections': connections
    }

    threads = []

    # Setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',int(sys.argv[1])))
    mySocket.listen(5)  #param represents the number of queued connections

    # Listening for connections
    while True:
        try:
            #This is the simple way to start this; we could also do a SELECT
            conn, address = mySocket.accept()
            logging.getLogger().info('Opened connection with %s ', address)
            #start a new thread
            lock = thread.allocate_lock()
            thread.start_new_thread(handler, (conn, lock, myData, address))
        except KeyboardInterrupt:
            mySocket.close()


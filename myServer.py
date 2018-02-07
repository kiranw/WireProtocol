'''
CS 262: Distributed Systems

Created on Feb 18, 2010

Restructured and re-factored by Jim Waldo, 2/17/2014
'''

import socket
import logging
import struct
from logging.config import dictConfig
import myServerReceive
import myServerSend
from myServerSend import unknown_opcode
import _thread as thread

version = '\x01'

# Opcodes to be sent by client
opcodes = {'\x10': myServerReceive.create_request,        # Create account <username>
           '\x20': myServerReceive.delete_request,        # Delete, only if logged in
           '\x30': myServerReceive.login_request,         # Login <username>, only if user exists
           '\x40': myServerReceive.logout_request,        # Logout, only if logged in
           '\x50': myServerReceive.send_message_request,  # Send message <dest_username> <message>
           '\x60': myServerReceive.collect_messages,      # Collect messages, only if logged in
           }

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
def handler(conn,lock, myData):
    #keep track of erroneous opcodes
    second_attempt = 0
    while True:
        #retrieve header
        try:
            netbuffer = conn.recv( 1024 )
        except:
            #close the thread if the connection is down
            thread.exit()
        #if we receive a message...
        if len(netbuffer) >= 6:
            #unpack it...
            header = struct.unpack('!cIc', netbuffer[0:6])
            #only allow correct version numbers and buffers that are of the appropriate length
            if header[0] == version and len(netbuffer) == header[1] + 6:
                opcode = header[2]
                #try to send packet to correct handler
                try:
                    opcodes[opcode](conn,netbuffer,myData,lock)
                #catch unhandled opcodes
                except KeyError:
                    if(second_attempt):
                        #disconnect the client
                        myServerSend.end_session_success(conn)
                        conn.close()
                        return
                    else:
                        #send incorrect opcode message
                        second_attempt = 1
                        unknown_opcode(conn)


if __name__ == '__main__':
    # Data structure for storing account information
    myData = dict()

    #setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',8080))
    mySocket.listen(5)  #param represents the number of queued connections

    #listening for connections
    while True:
        #This is the simple way to start this; we could also do a SELECT
        conn, address = mySocket.accept()
        logging.getLogger().info('Opened connection with %s ', address)
        #start a new thread
        lock = thread.allocate_lock()
        thread.start_new_thread(handler, (conn, lock, myData))

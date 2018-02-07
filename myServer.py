'''
CS 262: Distributed Systems

Created on Feb 18, 2010

Restructured and re-factored by Jim Waldo, 2/17/2014
'''

import socket
import myServerReceive
import myServerSend
from myServerSend import unknown_opcode
import thread

version = '\x01'
#opcode associations
opcodes = {'\x10': myServerReceive.create_request, 
           '\x20': myServerReceive.delete_request,
           '\x30': myServerReceive.deposit_request,
           '\x40': myServerReceive.withdraw_request,
           '\x50': myServerReceive.balance_request,
           '\x60': myServerReceive.end_session
           }

def recordConnect(log, addr):
    print 'Opened connection with ' + addr
    log.write('Opened connection with ' + addr + '\n')
    log.flush()
    
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
            header = netbuffer.unpack('!cIc',netbuffer[0:6])
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
    #set up log
    log = open('log.txt', 'a')
    #data structure for storing account information
    myData = dict()

    #setup socket
    mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mySocket.bind(('',8080))
    mySocket.listen(5)  #param represents the number of queued connections

    #listening for connections
    while True:
        #This is the simple way to start this; we could also do a SELECT
        conn, address = mySocket.accept()
        #log connection
        recordConnect(log, str(address)) 
        #start a new thread
        lock = thread.allocate_lock()
        thread.start_new_thread(handler, (conn, lock, myData))

    log.close()
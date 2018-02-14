'''
CS 262: Distributed Systems
Created on Feb 18, 2010
Altered Feb. 20, 2014
------------------------------

Adapted by Mali and Kiran for Assignment 1, CS262
'''

import socket
import myClientSend
from myClientReceive import *
#from myServerSend import *
import sys
from struct import unpack
from threading import Thread 

version = b'\x01'


# Opcode associations received by the Server
# x11 - create_success - Delievered on success in account creation
# x12 - general_failure
# x21 - delete_success - Delievered on success in account deletion
# x22 - general_failure
# x31 - login_success - Delievered on success in login
# x32 - general_failure
# x41 - logout_success - Delievered on success in logout
# x42 - general_failure
# x51 - send_message_success - Delievered on success for sending messages
# x52 - general_failure
# x61 - collect_messages_success - Delievered on success in collecting undelivered messages
# x62 - general_failure
# x63 - unknown_opcode

opcodes = {b'\x11': create_success,
           b'\x12': general_failure,  
           b'\x21': delete_success,
           b'\x22': general_failure,
           b'\x31': login_success,
           b'\x32': general_failure,
           b'\x41': logout_success,
           b'\x42': general_failure,
           b'\x51': send_message_success,
           b'\x52': general_failure,
           b'\x61': collect_messages_success,
           b'\x62': general_failure,
           b'\x71': unknown_opcode,
           b'\x72': no_new_messages
           }

def getInput(mySocket):
    print('''
CONNECTED TO MESSAGE SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Login to Account
    (4) Logout
    (5) Send a Message
    (6) Collect Undelivered Messages
    ''')
    netBuffer = input('>> ')
    return netBuffer

def processInput(netBuffer):
    #create
    if netBuffer == str(1):
        myClientSend.create_request(mySocket)
        
    #delete
    elif netBuffer == str(2):
        myClientSend.delete_request(mySocket)
        
    #login
    elif netBuffer == str(3):
        myClientSend.login_request(mySocket)
        
    #logout
    elif netBuffer == str(4):
        myClientSend.logout_request(mySocket)
        
    #send a message to a user
    elif netBuffer == str(5):
        myClientSend.send_message_request(mySocket)
        
    #collect undelivered messages 
    elif netBuffer == str(6):
        myClientSend.collect_messages_request(mySocket)
        
    return
        
def getResponse(mySocket):
    #wait for server responses...
    while True:
        try:
            retBuffer = mySocket.recv( 1024 )
        except:
            #close the client if the connection is down
            print("ERROR: connection down")
            sys.exit()
            
        if len(retBuffer) != 0:            
            header = unpack('!cIc',retBuffer[0:6])

            #only allow correct version numbers
            if header[0] == version:
                opcode = header[2]
                
                #send packet to correct handler
                try:
                    opcodes[opcode](mySocket,retBuffer)
                except KeyError:
                    break
            break
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
    except:
        print("ERROR: could not connect to " + myHost + ":" + myPort)
        sys.exit()

    while True:
        netBuffer = getInput(mySocket)

        #menu selection and function priming
        processInput(netBuffer)
        getResponse(mySocket)

    mySocket.close()





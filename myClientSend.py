'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit

#create new account
def create_request(conn):
    
    print "CREATING AN ACCOUNT \n"
    print "enter a starting balance:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    print "enter a an account number 1-100(input 0 for a random number):"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        elif(netBuffer == 0):
            act = -1
            break
    
    send_message('\x01' + pack('!I',8) + '\x10' + pack('!II',bal,act),conn)
    
    return

#delete an existing account
def delete_request(conn):
    print "DELETING AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    
    send_message('\x01' + pack('!I',4) + '\x20' + pack('!I',act),conn)
    return

#deposit to an existing account
def deposit_request(conn):
    print "DEPOSITING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    print "enter an amount to deposit:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    send_message('\x01' + pack('!I',8) + '\x30' + pack('!II',act,bal),conn)
    return

#withdraw from an existing account
def withdraw_request(conn):
    print "WITHDRAWING SOME DOUGH \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
        
    print "enter an amount to withdraw:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
        
    send_message('\x01' + pack('!I',8) + '\x40' + pack('!II',act,bal),conn)
    return

#withdraw from an existing account
def balance_request(conn):
    print "CHECKING THE BALANCE OF AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        
        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    send_message('\x01' + pack('!I',4) + '\x50' + pack('!I',act),conn)
    return

#end a session
def end_session(conn):
    send_message('\x01\x00\x00\x00\x00\x60',conn)
    return

def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print "ERROR: connection down"
            exit()
    return

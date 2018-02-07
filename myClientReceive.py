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
    print "\nERROR: " + netBuffer[8:8+strlen]
    return

#create new account
def create_success(conn, netBuffer):
    values = unpack('!I',netBuffer[6:10])
    print "Account creation successful " + str(values[0])
    return

#delete an existing account
def delete_success(conn, netBuffer):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn,netBuffer):
    values = unpack('!I',netBuffer[6:10])
    print "Deposit success. The updated balance: " + str(values[0])
    return

#withdraw from an existing account
def withdraw_success(conn,netBuffer):
    values = unpack('!I',netBuffer[6:10])
    print "Withdrawal success. The updated balance: " + str(values[0])
    return

#withdraw from an existing account
def balance_success(conn,netBuffer):
    values = unpack('!I',netBuffer[6:10])
    print "The balance of that account is: " + str(values[0])
    return

#end a session
def end_session_success(conn,netBuffer):
    print "SHUTTING DOWN"
    conn.close()
    exit()
    return

#handle invalid opcodes
def unknown_opcode(conn):
    print "ERROR: INCORRECT OPCODE"
    return
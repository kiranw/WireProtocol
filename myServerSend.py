'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''

from struct import pack

def general_failure(conn, type, reason):
    
    #find the appropriate opcode to send for particular errors
    if type == 'create':
        typebyte = b'\x12'
    elif type == 'delete':
        typebyte = b'\x22'
    elif type == 'login':
        typebyte = b'\x32'
    elif type == 'logout':
        typebyte = b'\x42'
    elif type == 'send_message':
        typebyte = b'\x52'
    elif type == 'receive_messages':
        typebyte = b'\x62'
    
    #encode and send the string
    utf = reason.encode('utf-8')
    utflen = len(utf)
    conn.send(b'\x01' + pack('!I',2 + utflen) + typebyte + pack('!h',utflen) + utf)
    return

#create new account
def create_success(conn):
    # conn.send('\x01' + pack('!I',4) +'\x11' + pack('!100p',act))
    conn.send(b'\x01\x00\x00\x00\x00\x11')
    return

#delete an existing account
def delete_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x21')
    return

def login_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x31')
    # conn.send(b'\x01' + pack('!I',4) + b'\x31' + pack('!I',bal))
    return

def logout_success(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x41')
    # conn.send(b'\x01' + pack('!I',4) + b'\x41' + pack('!I',bal))
    return

def send_message_success(conn,received):
    # If received is true, the destination user was active
    # Else, the user's messages are collected in the server
    # received is a boolean - do we want to send it as such? is it worth even notifying the client of this?
    conn.send(b'\x01' + pack('!I',30) + b'\x51' + pack('!30p',received))
    return

def collect_messages_success(conn, messages):
    # What happens in the case of partial failure to send a message?
    for message in messages:
        conn.send(b'\x01' + pack('!I',300) + b'\x61' + pack('!300p',message))
    return

#handle invalid opcodes
def unknown_opcode(conn):
    conn.send(b'\x01\x00\x00\x00\x00\x72')
    return



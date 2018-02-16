import struct

import message
from message import AbstractMessage, make_message

#
# Generic message types
#


class GenericSingleTextMessage(AbstractMessage):
    """Generic message type that handles string_length +
    arbitrary_length_string type messages"""

    @classmethod
    def _encode(cls, text):
        encoded_text = text.encode("utf-8")
        length = len(encoded_text)
        return struct.pack('!H', length) + encoded_text

    @classmethod
    def _decode(cls, binary_data):

        length = struct.unpack('!H', binary_data[:2])[0]

        if len(binary_data[2:]) != length:
            raise ValueError("Length reported for string is {}, got {}".format(length, len(binary_data[2:])))

        # Read amount specified
        text = binary_data[2:].decode("utf-8")
        return (text, )


class GenericFailResponse(GenericSingleTextMessage):
    """Generic fail response that handles string_length +
    arbitrary_length_string type messages"""
    pass


#
# Client-to-server Requests
#

class CreateRequest(AbstractMessage):
    """Create account <username>"""

    OPCODE = b'\x10'
    PACK_FORMAT = "!100p"


class DeleteRequest(AbstractMessage):
    """Delete, only if logged in"""

    OPCODE = b'\x20'
    PACK_FORMAT = ""


class LoginRequest(AbstractMessage):
    """Login <username>, only if user exists"""

    OPCODE = b'\x30'
    PACK_FORMAT = "!100p"


class LogoutRequest(AbstractMessage):
    """Logout, only if logged in"""

    OPCODE = b'\x40'
    PACK_FORMAT = ""


class SendMessageRequest(AbstractMessage):
    """Send message <dest_username> <message>"""

    OPCODE = b'\x50'
    PACK_FORMAT = None

    @classmethod
    def _encode(cls, dest_account, text):
        return struct.pack('!100p', bytes(dest_account, 'ascii')) +\
               struct.pack('!255p', bytes(text, 'ascii'))

    @classmethod
    def _decode(cls, binary_data):
        dest_account = struct.unpack('!100p', binary_data[:100])[0].decode("ascii")
        text = struct.unpack('!255p', binary_data[100:])[0].decode("ascii")
        return (dest_account, text)


class CollectMessageRequest(AbstractMessage):
    """Collect messages, only if logged in."""

    OPCODE = b'\x60'
    PACK_FORMAT = ""


#
# Server-to-client Responses
#


class CreateSuccessResponse(AbstractMessage):
    OPCODE = b'\x11'
    PACK_FORMAT = ""


class CreateFailResponse(GenericFailResponse):
    OPCODE = b'\x12'
    PACK_FORMAT = ""


class DeleteSuccessResponse(AbstractMessage):
    OPCODE = b'\x21'
    PACK_FORMAT = ""


class DeleteFailResponse(GenericFailResponse):
    OPCODE = b'\x22'
    PACK_FORMAT = ""


class LoginSuccessResponse(AbstractMessage):
    OPCODE = b'\x31'
    PACK_FORMAT = ""


class LoginFailResponse(GenericFailResponse):
    OPCODE = b'\x32'
    PACK_FORMAT = ""


class LogoutSuccessResponse(AbstractMessage):
    OPCODE = b'\x41'
    PACK_FORMAT = ""


class LogoutFailResponse(GenericFailResponse):
    OPCODE = b'\x42'
    PACK_FORMAT = ""


class SendSuccessResponse(GenericSingleTextMessage):
    OPCODE = b'\x51'
    PACK_FORMAT = ""


class SendFailResponse(GenericSingleTextMessage):
    OPCODE = b'\x52'
    PACK_FORMAT = ""


class SendQueuedResponse(GenericSingleTextMessage):
    """User offline but server queued the message"""
    OPCODE = b'\x53'
    PACK_FORMAT = ""


class CollectSuccessResponse(GenericSingleTextMessage):
    OPCODE = b'\x61'
    PACK_FORMAT = ""


class CollectFailResponse(GenericFailResponse):
    OPCODE = b'\x62'
    PACK_FORMAT = ""


class CollectNoNewResponse(AbstractMessage):
    """No new messages to collect"""
    OPCODE = b'\x63'
    PACK_FORMAT = ""


class EndSessionResponse(GenericSingleTextMessage):
    OPCODE = b'\x98'
    PACK_FORMAT = ""


class UnknownMessageResponse(AbstractMessage):
    OPCODE = b'\x99'
    PACK_FORMAT = ""


# Create a mapping to see if responses match the type of request that was sent
REQUEST_RESPONSE_MAPPINGS = {
    "1": [CreateSuccessResponse, CreateFailResponse],
    "2": [DeleteSuccessResponse, DeleteFailResponse],
    "3": [LoginSuccessResponse, LoginFailResponse],
    "4": [LogoutSuccessResponse, LogoutFailResponse],
    "5": [SendSuccessResponse, SendFailResponse, SendQueuedResponse],
    "6": [CollectSuccessResponse, CollectFailResponse, CollectNoNewResponse]
}
 
# Return True if the response type matches the behavior expected, to see if messages are caught up on client side
def matchingRequestResponse(menu_number, message_type):
    return message_type in REQUEST_RESPONSE_MAPPINGS[menu_number]

#
# Lookup data structures to find messages easily
#
REQUEST_MESSAGES = [
    CreateRequest,
    DeleteRequest,
    LoginRequest,
    LogoutRequest,
    SendMessageRequest,
    CollectMessageRequest
]

RESPONSE_MESSAGES = [
    CreateSuccessResponse,
    CreateFailResponse,
    DeleteSuccessResponse,
    DeleteFailResponse,
    LoginSuccessResponse,
    LoginFailResponse,
    LogoutSuccessResponse,
    LogoutFailResponse,
    SendSuccessResponse,
    SendFailResponse,
    SendQueuedResponse,
    CollectSuccessResponse,
    CollectFailResponse,
    CollectNoNewResponse,
    UnknownMessageResponse
]

MESSAGES = REQUEST_MESSAGES + RESPONSE_MESSAGES

# To look up Messages by opcode
opcode_table = {m.OPCODE: m for m in MESSAGES}


def get_message_by_opcode(opcode):
    return opcode_table.get(opcode, None)


#
# Message parsing / receiving functions
#

def receive_message(socket):
    """Given a socket, read a message off of it: first the header, and then
    using the size from the header, read the body."""

    # Receive 6 bytes for the header
    header = socket.recv(6)

    # Parse header
    opcode, message_length = message.parse_header(header)

    # Receive the rest of the message based on the header
    message_body = socket.recv(message_length)

    # Look up opcode
    message_type = get_message_by_opcode(opcode)

    # Make sure opcode is valid
    if message_type is None:
        raise ValueError("Invalid opcode {}".format(opcode))

    return message_type, message_type._decode(message_body)


def parse_message(binary_data):
    """This is mostly for testing, you'll probably need receive_message
    instead."""

    if len(binary_data) < 6:
        raise ValueError("Your message is less than 6 bytes, meaning it can't fit a header and therefore can't be valid")

    message_header = binary_data[:6]
    message_body = binary_data[6:]

    opcode, message_length = message.parse_header(message_header)
    message_type = get_message_by_opcode(opcode)

    if message_type is None:
        raise ValueError("Invalid opcode {}".format(opcode))

    return message_type, message_type._decode(message_body)

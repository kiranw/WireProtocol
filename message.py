import struct


VERSION = b'\x01'


def make_header(opcode, message_length, version=VERSION):
    """Make a header binary string: version + length + opcode"""
    return version + struct.pack('!I', message_length) + opcode


def parse_header(binary_data, version=VERSION):
    """Parse a header binary string: version + length + opcode"""

    # Raise exception if version is wrong
    curr_version = binary_data[0:1]
    if curr_version != version:
        raise ValueError("Protocol version {} is not what we are using ({}).".format(curr_version, version))

    if len(binary_data) != 6:
        raise ValueError("Header must be 6 bytes, got {}.".format(len(binary_data)))

    message_length, opcode = struct.unpack("!Ic", binary_data[1:])
    return opcode, message_length


def make_message(message_type, *args, **kwargs):
    """Make a message binary string: header + message"""

    # Call the message class' encode function to do message-specific stuff
    message_body = message_type._encode(*args, **kwargs)

    # Option to not add header
    if not kwargs.get("header", True):
        return message_body

    # Make a header for the message
    message_length = len(message_body)
    message_header = make_header(message_type.OPCODE, message_length)

    return message_header + message_body


class AbstractMessage(object):
    """This is an abstract base class that handles encoding / decoding messages
    using struct.pack, including the header. Look at subclasses for specific
    message implementations."""

    OPCODE = None
    PACK_FORMAT = None

    @classmethod
    def _encode(cls, *args):
        """Default implementation will look for PACK_FORMAT and do
        struct.pack() with it and pass the arguments in. For more complicated
        behavior you'll have to override this."""

        if cls.PACK_FORMAT is None:
            raise NotImplementedError("""The message class {} does not have a property called PACK_FORMAT""".format(cls))

        # If any arguments are strings, encode them to binary as utf-8
        args = list(args)
        for i, arg in enumerate(args):
            if type(arg) is str:
                args[i] = arg.encode("utf-8")

        return struct.pack(cls.PACK_FORMAT, *args)

    @classmethod
    def _decode(cls, binary_data):
        """Default implementation will look for PACK_FORMAT and do
        struct.unpack() with it and pass the arguments in. For more complicated
        behavior you'll have to override this."""

        if cls.PACK_FORMAT is None:
            raise NotImplementedError("""The message class {} does not have a property called PACK_FORMAT""".format(cls))

        unpacked = struct.unpack(cls.PACK_FORMAT, binary_data)

        # If any results are strings, encode them to binary as utf-8
        for i, arg in enumerate(unpacked):
            if type(arg) is str:
                unpacked[i] = arg.decode("utf-8")

        return unpacked

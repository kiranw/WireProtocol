# Design Exercise: Wire protocols

By: Mali Akmanalp, Kiran Wattamwar

## Requirements

This package runs only with Python 3, not Python 2. You don't need any extra
packages. You can test to see what's installed by trying to run `python3
--version` (the default on systems with both 2 and 3 installed) or `python
--version` (when only python 3 is installed). If not, you can get it from your
distribution's package manager (e.g. apt or homebrew) or from [the python website](https://www.python.org/downloads/).

## Instructions

If your python executable is named `python`, just make sure you're calling that
instead in all the commands below.

First you must run the server by invoking: `python3 myServer.py <port>`.
Instead of `<port>` place in a port number greater than 1024, for example 8080.

Now ensure that your server is accessible from wherever you're connecting the
client. If this is the same computer this shouldn't be an issue, but for
different computers you might want to test that the IP address is accessible.
One way to do this could be to run `ping <serveripaddress>`, which should give
you back a response with how many milliseconds it took.

Once that's done, run a client by invoking it with the IP and the port you
chose for the server `python3 myClient.py <serveripaddress> <port>`. You should
be greeted with a welcome message and a menu. Connect multiple clients to test
messaging back and forth.

## Code Structure

- protocol.py: Handle encoding and parsing of messages between the client and server
- message.py: Encode and decode parts of messages, generate headers
- myServer.py / myClient.py: Main event loop for client and server
- myServerSend.py / myClientSend.py: Functions to send messages
- myServerReceive.py / myClientReceive.py: Event handlers that describe what to
  do when the client / server receives a message

## Protocol Description

A message consists of a fixed-size header and an arbitrary length body.

```
message = header + body[bytes]
header = version[char] + message_length_bytes[uint64] + opcode[char]
```

A 6-byte header consists of a 1-byte version number which determines the
protocol version that the message is associated with. This can be used to
reject or handle differently messages from different versions of the software.

This is followed by a message length (in bytes, not including the header
itself), and a 1-byte message opcode. The opcode determines how the message
body should be interpreted.

## Message Specifics

The file `protocol.py` contains a series of classes that specifies each message
opcode and how it should be encoded and decoded. Both the server and the client
use these classes to decode and encode messages, and then perform actions based
on which message they got. Note that the actions themselves are not part of the
message description and are dealt with in the client / server code separately
(in `myClientReceive.py` and `myServerReceive.py`).

Each message class is a subclass of the `AbstractMessage` class specified in
`message.py`, and has an OPCODE which specifies the opcode byte that it will
interpret and PACK_FORMAT which specifies how to decode the message body into
python types, specified in python's [struct.pack
mini-language](https://docs.python.org/3/library/struct.html#format-characters).
This allows for quickly specifying sequences of standard types without
redundant type conversion code.

Alternatively the PACK_FORMAT can be ignored and the `_encode()` and
`_decode()` functions can be overridden to manually unpack the bytes. This is
useful for more complex types of messages e.g. variable length strings.

Alternatively the message can be a subclass of a pre-created generic message
type like `GenericSingleTextMessage` or `GenericFailResponse` which helps
reduce redundant code.

## Technical Decisions

- We maintain an explicit mapping of request opcodes to expected response
  opcodes to better handle out of order messages.
- The server maintains state for each connected client (by socket), including
  the currently logged in user on that socket. Server state is maintained
  consistent with a lock around any data structure that modifies the state
  variables. This simplifies client code, which acts like a dumb terminal.
- Messages to logged in users are immediately delivered to the user socket. New
  messages are read and printed every time the client performs any operation.
- Messages to non logged in users are kept on the server in each user's own
  queue.
- Account names can only be alphanumeric and less than 100 characters.
- Fetching undelivered messages is accomplished by the server responding to the
  fetch request with multiple messages to the client, as if they had just been
  sent.
- Deleted users get their persistent server state (including messages) removed.
  Users can only delete themselves and only when online.

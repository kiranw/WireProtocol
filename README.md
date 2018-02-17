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
- myServer.py: Main server logic
- myClient.py: Main client logic
- myServerSend.py: Send functions for every message type for the server
- myClientSend.py: Send functions for every message type for the client
- myServerReceive.py: Handling routines for every message type for the server
- myClientReceive.py: Handling routines for every message type for the server

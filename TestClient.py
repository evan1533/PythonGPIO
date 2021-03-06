import socket
import sys

# Create a TCP/IP socket

# Connect the socket to the port where the server is listening
sock = socket.socket();
server_address = ('172.24.66.145', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    # Send data
    message = b'1'
    print('sending {!r}'.format(message))
    sock.send(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while True:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()

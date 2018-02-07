import socket
import sys
import pyglet

player = pyglet.media.Player();
neva = pyglet.media.load('NeverGonnaGiveYouUp.wav');
player.queue(neva);

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('172.24.66.145', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            playData = int(data);
            if playData == 1:
                player.play();
            elif playData == 0:
                player.pause();

    finally:
        # Clean up the connection
        connection.close()

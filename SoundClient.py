#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import pyglet
import threading
import socket
import sys

MS = 17
GPIO.setmode(GPIO.BCM)
player = pyglet.media.Player();
neva = pyglet.media.load('NeverGonnaGiveYouUp.wav');
player.queue(neva);
playSound = 0;
def setup():
	GPIO.setup(MS, GPIO.IN)
	playSound = 0;
	
  
def loop():
        playSound = 0;
	while True:
		tmp = GPIO.input(MS);
		print('%d %d',tmp,playSound);
		if tmp != playSound:
                    playSound = tmp;
                    sendPlayMessage(b''+str(playSound));
		time.sleep(0.2)


# Create a TCP/IP socket
# Connect the socket to the port where the server is listening
sock = socket.socket();
server_address = ('172.24.66.145', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

def sendPlayMessage(mess):      
    try:

        # Send data
        print('sending {!r}'.format(mess))
        sock.send(mess)

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


if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	


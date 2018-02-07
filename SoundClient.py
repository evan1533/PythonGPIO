#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import pyglet
import threading
import socket
import sys

MS = 17
GPIO.setmode(GPIO.BCM)

def setup():
	GPIO.setup(MS, GPIO.IN)
	playSound = 0;
	
  
def loop():
        playSound = 0;
        time.sleep(10)
	while True:
		tmp = GPIO.input(MS);
		# print(tmp,playSound);
		if tmp != playSound:
                    playSound = tmp;
                    sendPlayMessage(b''+str(playSound));


# Create a TCP/IP socket
# Connect the socket to the port where the server is listening
sock = socket.socket();
server_address = ('172.24.66.145', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

def sendPlayMessage(mess):
        # Send data
        print('sending {!r}'.format(mess))
        sock.send(mess)



if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
                print('closing socket')
                sock.close()
		pass	


#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import pyglet
import threading
import socket
import sys

MS = 17

def setup():
	playSound = 0;
	
  
def loop():
        playSound = 0;
        print("ARMING IN 10 SECONDS");
        time.sleep(10)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MS, GPIO.IN)
        print("ARMED");
        while GPIO.input(MS) == 1:
                print("Waiting for sensor");
        print("READY");
	while True:
		# print(tmp,playSound);
		if playSound != GPIO.input(MS):
                    playSound = GPIO.input(MS);
                    sendPlayMessage(b''+str(GPIO.input(MS)));
		time.sleep(0.1)


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


#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

MS = 17
GPIO.setmode(GPIO.BCM)

def setup():
	GPIO.setup(MS, GPIO.IN)
  
def loop():
	status = 1
	while True:
		tmp = GPIO.input(DO);
		print tmp
		
		time.sleep(0.2)

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt: 
		pass	

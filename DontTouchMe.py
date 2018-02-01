#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
TRIG = 12
ECHO = 13
LedPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def setup():
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(TRIG, GPIO.OUT)
    	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
def distance():
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)
	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)
	time1 = 0
	time2 = 0
	while GPIO.input(ECHO) == 0:
		a = 0
		time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
		time2 = time.time()
	during = time2 - time1
	during = during * 340 / 2 * 100
	if during < 15:
		print '...led on'
		GPIO.output(LedPin, GPIO.LOW)  # led on
	else:
		print '...led off'
		GPIO.output(LedPin, GPIO.HIGH)  # led off
	return during
    
def loop():
	while True:
		dis = distance()
	    	print dis, 'cm'
	    	print ''
        	time.sleep(0.3)
        
def destroy():
	GPIO.cleanup()
	GPIO.output(LedPin, GPIO.LOW)   

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()



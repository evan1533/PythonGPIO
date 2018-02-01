#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
TRIG = 12
ECHO = 13
BuzzPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
global Buzz						# Assign a global variable to replace GPIO.PWM 
Buzz = GPIO.PWM(BuzzPin, 440)	# 440 is initial frequency.


def setup():
    	GPIO.setmode(GPIO.BOARD)
    	GPIO.setup(TRIG, GPIO.OUT)
    	GPIO.setup(ECHO, GPIO.IN)
	GPIO.setup(BuzzPin, GPIO.OUT)
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
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
		print 'GET BACK HETHAN!'
		Buzz.start(100)
	else:
		GPIO.output(BuzzPin, GPIO.HIGH)  # led off
		Buzz.stop()
	return during
    
def loop():
	while True:
		dis = distance()
	    	print dis, 'cm'
	    	print ''
        	time.sleep(0.3)
        
def destroy():
	Buzz.stop()					# Stop the buzzer
	GPIO.output(Buzzer, 1)		# Set Buzzer pin to High
	GPIO.cleanup()	

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()



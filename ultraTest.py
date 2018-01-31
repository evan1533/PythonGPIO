#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
TRIG = 11
ECHO = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
ultraClean = False

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
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
    if time1 != 0 and time2 != 0:
        if during >2 and during <4:
            ultraClean = True
            GPIO.cleanup()
    return during * 340 / 2 * 100
    
def loop():
    while True:
        if not ultraClean:
            dis = distance()
            print dis, 'cm'
            print ''
        time.sleep(0.3)
        
def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

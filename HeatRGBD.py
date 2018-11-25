#!/usr/bin/env python
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import math

DO = 11
GPIO.setmode(GPIO.BCM)

R = 22                                                                                                                                  
G = 23
B = 24
max_green = 200;
def setup(Rpin, Gpin, Bpin):
	global pins
	global p_R, p_G, p_B
	pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
	ADC.setup(0x48)
	GPIO.setup(DO, GPIO.IN)
	#GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	for i in pins:
		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
		GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
	
	p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
	p_G = GPIO.PWM(pins['pin_G'], 1999)
	p_B = GPIO.PWM(pins['pin_B'], 5000)
	
	p_R.start(100)      # Initial duty Cycle = 0(leds off)
	p_G.start(100)
	p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off():
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0

	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)

def colorFromTemp(temp):
	if temp >=82:
		r = 255
		g = 200 - int((temp-82)*7.14285)
		b = 0
	elif temp >= 55:
		r = 255
		g = 200
		b = 255 - int( (temp-55)*7.407407)
	elif temp >= 27:
		r = 0 + int( (temp-27)*7.14285 )
		g = 200
		b = 255
	elif temp >= 0:
		r = 0
		g = 0 + int( (temp)*7.14285 )
		b = 255
	col = (r << 16) + (g << 8) + b
	print(temp, r, g, b, " -> ", hex(col))
	return col

def loop():
	hit_zero = False
	#Middle Temperature is 55
	temp = 55
	while True:
		analogVal = ADC.read(0)
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		temp = ((temp - 273.15) * (9/5)) + 32
		print('temperature = ', temp, 'F')
		color = colorFromTemp(temp);
		setColor(color)
		time.sleep(0.2)

def destroy():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	off()
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup(R, G, B)
		loop()
	except KeyboardInterrupt:
		destroy()

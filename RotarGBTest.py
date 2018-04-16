#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

RoAPin = 11    # CLK Pin
RoBPin = 12    # DT Pin
BtnPin = 13    # Button Pin

R = 15
G = 16
B = 18

r_val = 0
g_val = 0
b_val = 0

globalCounter = 0

flag = 0
Last_RoB_Status = 0
Current_RoB_Status = 0

def rgb2hex(rgb):
	return '0x%02x%02x%02x' % rgb

def setup(Rpin, Gpin, Bpin):
	
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(RoAPin, GPIO.IN)    # input mode
	GPIO.setup(RoBPin, GPIO.IN)
	GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	global pins
	global p_R, p_G, p_B
	pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
	for i in pins:
		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
		GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
	
	p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
	p_G = GPIO.PWM(pins['pin_G'], 1999)
	p_B = GPIO.PWM(pins['pin_B'], 5000)
	
	p_R.start(100)      # Initial duty Cycle = 0(leds off)
	p_G.start(100)
	p_B.start(100)


def rotaryDeal():
	global flag
	global Last_RoB_Status
	global Current_RoB_Status
	global globalCounter
	global r_val
	global g_val
	global b_val
	Last_RoB_Status = GPIO.input(RoBPin)
	while(not GPIO.input(RoAPin)):
		Current_RoB_Status = GPIO.input(RoBPin)
		flag = 1
	if flag == 1:
		flag = 0
		if (Last_RoB_Status == 0) and (Current_RoB_Status == 1):
			globalCounter = globalCounter + 1
			if(r_val+1<=255):
				r_val = r_val + 1;
			elif(g_val+1<=255):
				g_val = g_val + 1;
			elif(b_val+1<=255):
				b_val = b_val + 1;
		if (Last_RoB_Status == 1) and (Current_RoB_Status == 0):
			globalCounter = globalCounter - 1
			
def setColor(col):   # For example : col = 0x112233
	print(col.encode('hex'))
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0

	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)
	
def btnISR(channel):
	global globalCounter
	globalCounter = 0

def loop():
	global globalCounter
	global r_val
	global g_val
	global b_val
	tmp = 0	# Rotary Temperary

	GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=btnISR)
	while True:
		rotaryDeal()
		if tmp != globalCounter:
			print 'globalCounter = %d' % globalCounter
			tmp = globalCounter
			print(r_val, g_val, b_val)
			setColor(rgb2hex((r_val,g_val,b_val)))

def off():
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all led
		
def destroy():
	p_R.stop()
	p_G.stop()
	p_B.stop()
	off()
	GPIO.cleanup()             # Release resource



def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min




if __name__ == "__main__":
	try:
		setup(R, G, B)
		loop()
	except KeyboardInterrupt:
		destroy()

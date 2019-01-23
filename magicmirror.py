# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

import time
from neopixel import *
from random import randint
import argparse

import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT 	= 116	# Number of LED pixels
LED_PIN		= 18 	# GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ	= 800000 # LED sugbak frequency in hertz (usually 800 khz)
LED_DMA		= 10	# DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS	= 255	# Set to 0 for darkest and 255 for brightest
LED_INVERT	= False	# True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL	= 0	# set to '1' for GPIOs 13, 19, 41, 45 or 53

# Class to control LEDs
class Status:
    def __init__(self, actualMotionStatus, actualLightLvl):
	self.motionStatus = actualMotionStatus
	self.lightLvl = actualLightLvl
	self.motionTrigger = False
	self.led_mode = 0

    def checkLightLvl(self, actualLightLvl):
	if self.lightLvl != actualLightLvl:
	    if actualLightLvl == True:
		self.lightLvl = actualLightLvl
		return True
	    else:
		self.lightLvl = actualLightLvl
		return False
	else:
	    return self.lightLvl

    def checkMotion(self, actualMotionStatus):
	if self.motionStatus != actualMotionStatus:
	    self.motionStatus = actualMotionStatus

	    if actualMotionStatus == True:
		print "Ktos sie ruszyl!"
		self.motionTrigger = True
		return True
	    else:
		print "Nikogo nie ma!"
		return False
	else:
	    self.motionTrigger = False

	    if self.motionStatus == True:
		return True
	    else:
		return False

    def getMotionTrigger(self):
	if self.motionTrigger == True:
	    self.motionTrigger = False
	    return True
	else:
	    return False

    def checkpoint(self, actualMotionStatus, actualLightLvl):
	#if self.checkLightLvl(actualLightLvl) == True: # When we have night
	if self.checkMotion(actualMotionStatus) == False: # When nobody is move
	    return True  # Can animate

	return False # Can't animate

class Timer:
    def __init__(self, actualTime):
	self.blocked = False
	self.lastTime = 0
	self.duration = 0

    def checkTimer(self, actualTime, motion):
	print 'Actual Time in ms: ', actualTime
	print 'Last time + delay: ', self.lastTime + self.duration
	if self.blocked == True:
	    if (self.lastTime + self.duration) < actualTime:
		self.blocked = False
	    elif motion == True:
		self.setTimer(actualTime, 30)

    def setTimer(self, actualTime, howLong):
	self.lastTime = actualTime
	self.duration = howLong
	self.blocked = True

    def getBlocked(self):
	return self.blocked

def setColor(strip, color, brightness):
    for i in range(strip.numPixels()):
	strip.setPixelColor(i, color)
	strip.setBrightness(brightness)
	strip.show()

def fadeIn(strip, color, wait_ms=10):
    for i in range(255):
	for k in range(strip.numPixels()):
	    strip.setPixelColor(k, color)
	strip.setBrightness(i)
	strip.show()
	if lookingForMotion(strip) == True:
	    return False
	time.sleep(wait_ms/1000.0)
    return True

def fadeOut(strip, wait_ms=10):
    for i in range(255, 0, -1):
	strip.setBrightness(i)
	strip.show()
	if lookingForMotion(strip) == True:
	    return False
	time.sleep(wait_ms/1000.0)
    #status.led_mode = 0
    return True

def fadeOutFromCurrentBrightness(strip, wait_ms=10):
    for i in range(strip.getBrightness(), 0, -1):
	strip.setBrightness(i)
	strip.show()
	if lookingForMotion(strip) == True:
	    return False
	time.sleep(wait_ms/1000.0)
    return True

def snake(strip, length, wait_ms=5):
    tempColor = 0
    for i in range(strip.numPixels()):
	if (i + length) < strip.numPixels():
	    tempColor = strip.getPixelColor(i)
	    strip.setPixelColor(i + length, tempColor)
	else:
	    tempColor = strip.getPixelColor(i)
	    strip.setPixelColor(i + length - strip.numPixels(), tempColor)
	strip.setPixelColor(i, Color(0, 0, 0))
	strip.show()
	time.sleep(wait_ms/1000.0)
    strip.setPixelColor(length, tempColor)
    strip.show()
    time.sleep(wait_ms/1000.0)

def breath(strip, color, wait_ms=10): # idle animation
    """Breath effect"""

    startBrightness = 0
    stopBrightness = LED_BRIGHTNESS
    step = 1

    setColor(strip, Color(0,0,0), 0)

    if fadeIn(strip, color) == False:
	return False
    if fadeOut(strip) == False:
	return False

    setColor(strip, Color(0, 0, 0), 0)
    time.sleep(0.2)

def mirrorFall(strip, color, wait_ms=50):
    """Mirror Fall"""

    strip.setBrightness(255)

    x1 = 0
    x2 = 0
    iterations = 0

    if strip.numPixels() % 2 == 0:
	x1 = strip.numPixels() / 2 - 1
	x2 = strip.numPixels() / 2
	iterations = strip.numPixels() / 2 - 1
    else:
	x1 = strip.numPixels() / 2
	x2 = strip.numPixels() / 2
	iterations = strip.numPixels() / 2 + 1

    for i in range(iterations):
	strip.setPixelColor(x1 - i, color)
	strip.setPixelColor(x2 + i, color)
	strip.show()
	time.sleep(wait_ms/1000.0)

    fadeOut(strip)

def waterFall(strip, wait_ms=50): # Trigger animation
    """Waterfall"""
    setColor(strip, Color(0, 0, 0), 0)
    strip.setBrightness(255)
    strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))

    tempColor = 0
    for i in range(strip.numPixels()):
	for k in range(i, 0, -1):
	    tempColor = strip.getPixelColor(k - 1)
	    strip.setPixelColor(k, tempColor)
	strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))
	strip.show()
	time.sleep(wait_ms/1000.0)
    status.led_mode = 0
    fadeOut(strip)

def loading(strip, color, length, speed = 10.0):
    setColor(strip, Color(0, 0, 0), 0)
    strip.setBrightness(255)
    for i in range(length):
	strip.setPixelColor(i, color)

    for i in range(length, strip.numPixels(), 1):
	strip.setPixelColor(i, color)
	if i % 10 == 0:
	    speed = float(speed / 2.0)
        snake(strip, i, speed)

def checkStatus(actualMotionStatus, actualLightLvl):
    #if status.checkpoint(actualMotionStatus, actualLightLvl) == True:
    if actualLightLvl == True:
	if status.getMotionTrigger() == True:
	    if timer.getBlocked() == False:
		status.led_mode = 1
		waterFall(strip, 20)
	else:
	    status.led_mode = 0
	    breath(strip, Color(206, 135, 250))

def lookingForMotion(strip):
    timer.checkTimer(time.time(), GPIO.input(11))
    if timer.getBlocked() == False:
        if status.led_mode == 0:
	    if status.checkpoint(GPIO.input(11), GPIO.input(13)) == False:
		timer.setTimer(time.time(), 30)
		fadeOutFromCurrentBrightness(strip,1)
	        waterFall(strip, 20)
	        return True
    return False

status = 0
strip = 0
timer = 0

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    # Initialize GPIO with Motion Detector
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.IN)
    GPIO.setup(13, GPIO.IN)

    # Initialize Timer
    timer = Timer(time.time())

    # Initialize status Class (set actual value for all sensors)
    status = Status(GPIO.input(11), True)

    print ('Press Crtl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    oldState = 0
    status.led_mode = 1 # 0 - idle mode, 1 - trigger mode

    mirrorFall(strip, Color(99, 255, 71)) # First welcome animate

    try:
        while True:
	    #status.checkMotion(GPIO.input(11))
	    checkStatus(GPIO.input(11), GPIO.input(13))

            #print ('Light sky blue')
            #breath(strip, Color(206, 135, 250))
	    #print ('aqua marine')
	    #breath(strip, Color(255, 127, 212))
	    #print ('medium spring green')
	    #breath(strip, Color(250, 0, 154))
	    #print ('cyan')
	    #breath(strip, Color(255, 0, 255))
	    #print ('tomato')
	    #breath(strip, Color(99, 255, 71))
	    #print ('Yellow')
	    #breath(strip, Color(255, 255, 0))
	    #print ('Mirror Fall Blue')
	    #mirrorFall(strip, Color(0, 0, 255))
	    #print ('Waterfall')
	    #waterFall(strip)
	    #print ('Loading')
	    #loading(strip, Color(255, 255, 0), 5, 50.0)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 10)

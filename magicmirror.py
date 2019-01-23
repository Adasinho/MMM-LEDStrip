# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

import time
from neopixel import *
from random import randint
import argparse

import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT = 116  # Number of LED pixels
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000  # LED sugbak frequency in hertz (usually 800 khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


# Class to control LEDs
class Status:
    def __init__(self, actual_motion_status, actual_light_lvl):
        self.motionStatus = actual_motion_status
        self.lightLvl = actual_light_lvl
        self.motionTrigger = False
        self.led_mode = 0

    def checkLightLvl(self, actual_light_lvl):
        if self.lightLvl != actual_light_lvl:
            if actual_light_lvl:
                self.lightLvl = actual_light_lvl
                return True
            else:
                self.lightLvl = actual_light_lvl
                return False
        else:
            return self.lightLvl

    def check_motion(self, actual_motion_status):
        if self.motionStatus != actual_motion_status:
            self.motionStatus = actual_motion_status

            if actual_motion_status:
                print "Ktos sie ruszyl!"
                self.motionTrigger = True
                return True
            else:
                print "Nikogo nie ma!"
                return False
        else:
            self.motionTrigger = False

            if self.motionStatus:
                return True
            else:
                return False

    def getMotionTrigger(self):
        if self.motionTrigger:
            self.motionTrigger = False
            return True
        else:
            return False

    def checkpoint(self, actual_motion_status, actual_light_lvl):
        # if self.checkLightLvl(actualLightLvl) == True: # When we have night
        if not self.check_motion(actual_motion_status):  # When nobody is move
            return True  # Can animate

        return False  # Can't animate


class Timer:
    def __init__(self, actual_time):
        self.blocked = False
        self.lastTime = 0
        self.duration = 0

    def checkTimer(self, actual_time, motion):
        print 'Actual Time in ms: ', actual_time
        print 'Last time + delay: ', self.lastTime + self.duration
        if self.blocked:
            if (self.lastTime + self.duration) < actual_time:
                self.blocked = False
            elif motion:
                self.setTimer(actual_time, 30)

    def setTimer(self, actual_time, how_long):
        self.lastTime = actual_time
        self.duration = how_long
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
        if lookingForMotion(strip):
            return False
        time.sleep(wait_ms / 1000.0)
    return True


def fadeOut(strip, wait_ms=10):
    for i in range(255, 0, -1):
        strip.setBrightness(i)
        strip.show()
        if lookingForMotion(strip):
            return False
        time.sleep(wait_ms / 1000.0)
    # status.led_mode = 0
    return True


def fadeOutFromCurrentBrightness(strip, wait_ms=10):
    for i in range(strip.getBrightness(), 0, -1):
        strip.setBrightness(i)
        strip.show()
        if lookingForMotion(strip):
            return False
        time.sleep(wait_ms / 1000.0)
    return True


def snake(strip, length, wait_ms=5):
    temp_color = 0
    for i in range(strip.numPixels()):
        if (i + length) < strip.numPixels():
            temp_color = strip.getPixelColor(i)
            strip.setPixelColor(i + length, temp_color)
        else:
            temp_color = strip.getPixelColor(i)
            strip.setPixelColor(i + length - strip.numPixels(), temp_color)
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(wait_ms / 1000.0)
    strip.setPixelColor(length, temp_color)
    strip.show()
    time.sleep(wait_ms / 1000.0)


def breath(strip, color, wait_ms=10):  # idle animation
    """Breath effect"""

    startBrightness = 0
    stopBrightness = LED_BRIGHTNESS
    step = 1

    setColor(strip, Color(0, 0, 0), 0)

    if not fadeIn(strip, color):
        return False
    if not fadeOut(strip):
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
        time.sleep(wait_ms / 1000.0)

    fadeOut(strip)


def waterFall(strip, wait_ms=50):  # Trigger animation
    """Waterfall"""
    setColor(strip, Color(0, 0, 0), 0)
    strip.setBrightness(255)
    strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))

    temp_color = 0
    for i in range(strip.numPixels()):
        for k in range(i, 0, -1):
            temp_color = strip.getPixelColor(k - 1)
            strip.setPixelColor(k, temp_color)
        strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))
        strip.show()
        time.sleep(wait_ms / 1000.0)
    status.led_mode = 0
    fadeOut(strip)


def loading(strip, color, length, speed=10.0):
    setColor(strip, Color(0, 0, 0), 0)
    strip.setBrightness(255)
    for i in range(length):
        strip.setPixelColor(i, color)

    for i in range(length, strip.numPixels(), 1):
        strip.setPixelColor(i, color)
        if i % 10 == 0:
            speed = float(speed / 2.0)
        snake(strip, i, speed)


def checkStatus(actual_motion_status, actual_light_lvl):
    # if status.checkpoint(actualMotionStatus, actualLightLvl) == True:
    if actual_light_lvl:
        if status.getMotionTrigger():
            if not timer.getBlocked():
                status.led_mode = 1
                waterFall(strip, 20)
        else:
            status.led_mode = 0
            breath(strip, Color(206, 135, 250))


def lookingForMotion(strip):
    timer.checkTimer(time.time(), GPIO.input(11))
    if not timer.getBlocked():
        if status.led_mode == 0:
            if not status.checkpoint(GPIO.input(11), GPIO.input(13)):
                timer.setTimer(time.time(), 30)
                fadeOutFromCurrentBrightness(strip, 1)
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
    status.led_mode = 1  # 0 - idle mode, 1 - trigger mode

    mirrorFall(strip, Color(99, 255, 71))  # First welcome animate

    try:
        while True:
            # status.check_motion(GPIO.input(11))
            checkStatus(GPIO.input(11), GPIO.input(13))

        # print ('Light sky blue')
        # breath(strip, Color(206, 135, 250))
        # print ('aqua marine')
        # breath(strip, Color(255, 127, 212))
        # print ('medium spring green')
        # breath(strip, Color(250, 0, 154))
        # print ('cyan')
        # breath(strip, Color(255, 0, 255))
        # print ('tomato')
        # breath(strip, Color(99, 255, 71))
        # print ('Yellow')
        # breath(strip, Color(255, 255, 0))
        # print ('Mirror Fall Blue')
        # mirrorFall(strip, Color(0, 0, 255))
        # print ('Waterfall')
        # waterFall(strip)
        # print ('Loading')
        # loading(strip, Color(255, 255, 0), 5, 50.0)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)

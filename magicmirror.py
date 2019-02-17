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

USE_DUSK_DETECTOR = True

colors = [Color(99, 255, 71), Color(255, 127, 0), Color(144, 30, 255), Color(0, 148, 211), Color(250, 255, 205), Color(222, 255, 173)]
last_color_choose = 0

def dynamic_breath(led_strip, to_brightness=0):
    if to_brightness != 0:
        new_brightness = to_brightness
    else:
        new_brightness = randint(30, 225)

    direction = 1
    old_brightness = led_strip.getBrightness()
    if old_brightness < new_brightness:
        animation_range = abs(old_brightness - new_brightness)
    else:
        direction = -1
        animation_range = abs(old_brightness - new_brightness)

    for i in range(animation_range):
        old_brightness = old_brightness + direction
        led_strip.setBrightness(old_brightness)
        led_strip.show()
        time.sleep(5 / 1000.0)

    timer.check_timer(time.time(), GPIO.input(11))
    if not timer.get_blocked():
        status.led_mode = 0

def un_color(color):
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

def smooth_color_transition(led_strip, new_color, wait_ms=20):
    if strip.getBrightness() != 120:
        dynamic_breath(led_strip, 120)

    old_color = un_color(led_strip.getPixelColor(0))
    r = old_color[0]
    g = old_color[1]
    b = old_color[2]
    direction = [1, 1, 1]
    max = 0

    temp_new_color = un_color(new_color)

    if r > temp_new_color[0]:
        direction[0] = -1
    tmp = abs(r - temp_new_color[0])
    if tmp > max:
        max = tmp
    if g > temp_new_color[1]:
        direction[1] = -1
    tmp = abs(g - temp_new_color[1])
    if tmp > max:
        max = tmp
    if b > temp_new_color[2]:
        direction[2] = -1
    tmp = abs(b - temp_new_color[2])
    if tmp > max:
        max = tmp

    for i in range(max):
        if r != temp_new_color[0]:
            r = r + direction[0]
        if g != temp_new_color[1]:
            g = g + direction[1]
        if b != temp_new_color[2]:
            b = b + direction[2]

        old_color = Color(r, g, b)

        for k in range(led_strip.numPixels()):
            led_strip.setPixelColor(k, old_color)
        led_strip.show()
        if looking_for_motion(led_strip):
            return False
        time.sleep(wait_ms / 1000.0)

def idle_animation(led_strip):
    while True:
        tmp = randint(0, 5)
        if tmp != last_color_choose:
            smooth_color_transition(led_strip, colors[tmp])
            return True

def get_dusk_status():
    if USE_DUSK_DETECTOR:
        return GPIO.input(13)
    else:
        return True

# Class to control LEDs
class Status:
    def __init__(self, actual_motion_status, actual_light_lvl):
        self.motionStatus = actual_motion_status
        self.lightLvl = actual_light_lvl
        self.motionTrigger = False
        self.led_mode = 0

    def check_light_lvl(self, actual_light_lvl):
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

    def get_motion_trigger(self):
        if self.motionTrigger:
            self.motionTrigger = False
            return True
        else:
            return False

    def checkpoint(self, actual_motion_status, actual_light_lvl):
        # if self.check_light_lvl(actualLightLvl) == True: # When we have night
        if not self.check_motion(actual_motion_status):  # When nobody is move
            return True  # Can animate

        return False  # Can't animate


class Timer:
    def __init__(self):
        self.blocked = False
        self.lastTime = 0
        self.duration = 0

    def check_timer(self, actual_time, motion):
        print 'Actual Time in ms: ', actual_time
        print 'Last time + delay: ', self.lastTime + self.duration
        if self.blocked:
            if (self.lastTime + self.duration) < actual_time:
                self.blocked = False
            elif motion:
                self.set_timer(actual_time, 8)

    def set_timer(self, actual_time, how_long):
        self.lastTime = actual_time
        self.duration = how_long
        self.blocked = True

    def get_blocked(self):
        return self.blocked


def set_color(led_strip, color, brightness):
    for i in range(led_strip.numPixels()):
        led_strip.setPixelColor(i, color)
        led_strip.setBrightness(brightness)
        led_strip.show()


def fade_in(led_strip, color, wait_ms=10):
    for i in range(255):
        for k in range(led_strip.numPixels()):
            led_strip.setPixelColor(k, color)
        led_strip.setBrightness(i)
        led_strip.show()
        if looking_for_motion(led_strip):
            return False
        time.sleep(wait_ms / 1000.0)
    return True


def fade_out(led_strip, wait_ms=10):
    for i in range(255, 0, -1):
        led_strip.setBrightness(i)
        led_strip.show()
        if looking_for_motion(led_strip):
            return False
        time.sleep(wait_ms / 1000.0)
    # status.led_mode = 0
    return True


def fade_out_from_current_brightness(led_strip, wait_ms=10):
    for i in range(led_strip.getBrightness(), 0, -1):
        led_strip.setBrightness(i)
        led_strip.show()
        if looking_for_motion(led_strip):
            return False
        time.sleep(wait_ms / 1000.0)
    return True

def rooling(led_strip, iterations, wait_ms=20):
    for i in range(led_strip.numPixels() - 1, 1, -1):
        tmp = led_strip.getPixelColor(i - 1)
        led_strip.setPixelColor(i - 1, led_strip.getPixelColor(i))
        led_strip.setPixelColor(i, tmp)
    tmp = led_strip.getPixelColor(0)
    led_strip.setPixelColor(0, led_strip.getPixelColor(led_strip.numPixels() - 1))
    led_strip.setPixelColor(led_strip.numPixels() - 1, tmp)

    led_strip.show()
    time.sleep(wait_ms / 1000.0)

    timer.check_timer(time.time(), GPIO.input(11))
    if not timer.get_blocked():
        status.led_mode = 0
        fade_out(led_strip)


def snake(led_strip, length, wait_ms=5):
    temp_color = 0
    for i in range(led_strip.numPixels()):
        if (i + length) < led_strip.numPixels():
            temp_color = led_strip.getPixelColor(i)
            led_strip.setPixelColor(i + length, temp_color)
        else:
            temp_color = led_strip.getPixelColor(i)
            led_strip.setPixelColor(i + length - led_strip.numPixels(), temp_color)
        led_strip.setPixelColor(i, Color(0, 0, 0))
        led_strip.show()
        time.sleep(wait_ms / 1000.0)
    led_strip.setPixelColor(length, temp_color)
    led_strip.show()
    time.sleep(wait_ms / 1000.0)


def breath(led_strip, color, wait_ms=10):  # idle animation
    """Breath effect"""

    startBrightness = 0
    stopBrightness = LED_BRIGHTNESS
    step = 1

    set_color(led_strip, Color(0, 0, 0), 0)

    if not fade_in(led_strip, color):
        return False
    if not fade_out(led_strip):
        return False

    set_color(led_strip, Color(0, 0, 0), 0)
    time.sleep(0.2)


def mirror_fall(led_strip, color, wait_ms=50):
    """Mirror Fall"""

    led_strip.setBrightness(255)

    x1 = 0
    x2 = 0
    iterations = 0

    if led_strip.numPixels() % 2 == 0:
        x1 = led_strip.numPixels() / 2 - 1
        x2 = led_strip.numPixels() / 2
        iterations = led_strip.numPixels() / 2 - 1
    else:
        x1 = led_strip.numPixels() / 2
        x2 = led_strip.numPixels() / 2
        iterations = led_strip.numPixels() / 2 + 1

    for i in range(iterations):
        led_strip.setPixelColor(x1 - i, color)
        led_strip.setPixelColor(x2 + i, color)
        led_strip.show()
        time.sleep(wait_ms / 1000.0)

    fade_out(led_strip)


def water_fall(led_strip, wait_ms=50):  # Trigger animation
    """Waterfall"""
    set_color(led_strip, Color(0, 0, 0), 0)
    led_strip.setBrightness(255)
    led_strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))

    temp_color = 0
    for i in range(led_strip.numPixels()):
        for k in range(i, 0, -1):
            temp_color = led_strip.getPixelColor(k - 1)
            led_strip.setPixelColor(k, temp_color)
        led_strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))
        led_strip.show()
        time.sleep(wait_ms / 1000.0)
    status.led_mode = 0
    # fade_out(led_strip)


def loading(led_strip, color, length, speed=10.0):
    set_color(led_strip, Color(0, 0, 0), 0)
    led_strip.setBrightness(255)
    for i in range(length):
        led_strip.setPixelColor(i, color)

    for i in range(length, led_strip.numPixels(), 1):
        led_strip.setPixelColor(i, color)
        if i % 10 == 0:
            speed = float(speed / 2.0)
        snake(led_strip, i, speed)


def check_status(actual_motion_status, actual_light_lvl):
    # if status.checkpoint(actualMotionStatus, actualLightLvl) == True:
    if actual_light_lvl:
        if not timer.get_blocked():
            if status.get_motion_trigger():
                status.led_mode = 1
                #water_fall(strip, 20)
                dynamic_breath(strip)
            else:
                status.led_mode = 0
                #breath(strip, Color(206, 135, 250))
                idle_animation(strip)
        else:
            status.led_mode = 1
            #rooling(strip, 10)
            dynamic_breath(strip)



def looking_for_motion(led_strip):
    timer.check_timer(time.time(), GPIO.input(11))
    if not timer.get_blocked():
        if status.led_mode == 0:
            if not status.checkpoint(GPIO.input(11), get_dusk_status()):
                timer.set_timer(time.time(), 8)
                #fade_out_from_current_brightness(led_strip, 1)
                #water_fall(led_strip, 20)
                dynamic_breath(led_strip)
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
    timer = Timer()

    # Initialize status Class (set actual value for all sensors)
    status = Status(GPIO.input(11), True)

    print ('Press Crtl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    oldState = 0
    status.led_mode = 1  # 0 - idle mode, 1 - trigger mode

    mirror_fall(strip, Color(99, 255, 71))  # First welcome animate

    try:
        while True:
            # status.check_motion(GPIO.input(11))
            check_status(GPIO.input(11), get_dusk_status())

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
        # mirror_fall(strip, Color(0, 0, 255))
        # print ('Waterfall')
        # water_fall(strip)
        # print ('Loading')
        # loading(strip, Color(255, 255, 0), 5, 50.0)

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)

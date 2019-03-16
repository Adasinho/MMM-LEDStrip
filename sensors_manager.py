# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from status import *
from timer import *

import time
import RPi.GPIO as GPIO

GPIO_MOTION_SENSOR = 11
GPIO_LIGHT_SENSOR = 13
USE_DUSK_DETECTOR = True

def get_actual_motion_status():
    return GPIO.input(GPIO_MOTION_SENSOR)

def get_actual_light_status():
    return GPIO.input(GPIO_LIGHT_SENSOR)

def init():
    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_MOTION_SENSOR, GPIO.IN)
    GPIO.setup(GPIO_LIGHT_SENSOR, GPIO.IN)

class SensorsManager:
    def __init__(self):
        init()
        self.timer = Timer()
        self.status = Status(get_actual_motion_status(), True)
        self.last_light_status = get_actual_light_status()  # False - day, True - night
        self.dayTime = False

    # If use dusk detector, then return True if we have night or False when day
    def get_dusk_status(self, led_strip):
        if USE_DUSK_DETECTOR:
            actual_light_status = get_actual_light_status()
            if actual_light_status != self.last_light_status:
                if not actual_light_status:
                    self.dayTime = True
                self.dayTime = False
                self.last_light_status = actual_light_status
            return actual_light_status
        else:
            return True

    def looking_for_motion(self, led_strip):
        self.timer.check_timer(time.time(), get_actual_motion_status())
        if not self.timer.get_blocked():
            if self.status.led_mode == 0:
                if not self.status.checkpoint(get_actual_motion_status(), self.get_dusk_status(led_strip)):
                    self.timer.set_timer(time.time(), 8)
                    return True
        return False

    # Decide which animation can be show now, depends of time and light level
    def check_status(self, led_strip):
        actual_light_lvl = self.get_dusk_status(led_strip)
        if actual_light_lvl:
            if not self.timer.get_blocked():
                if self.status.get_motion_trigger():
                    self.status.led_mode = 1
                    return 1
                else:
                    if not sleep_time():
                        self.status.led_mode = 0
                        return 2
            else:
                self.status.led_mode = 1
                return 1
        return -1
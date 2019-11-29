# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from status import *
from timer import *


import shared_variables
import time


class SensorsManager:
    def __init__(self, actual_light_status):
        self.timer = Timer()
        self.status = Status(True)
        self.last_light_status = actual_light_status  # False - day, True - night

    # If use dusk detector, then return True if we have night or False when day
    def get_dusk_status(self, actual_light):
        if shared_variables.USE_DUSK_DETECTOR:
            actual_light_status = actual_light
            if actual_light_status != self.last_light_status:
                self.last_light_status = actual_light_status
            return actual_light_status
        else:
            return True

    def looking_for_motion(self, actual_motion_status, actual_light_status):
        self.timer.check_timer(time.time(), actual_motion_status)
        if not self.timer.get_blocked():
            if not self.status.animationOnProgress:
                # If can't animate
                if not self.status.checkpoint(actual_motion_status, self.get_dusk_status(actual_light_status)):
                    self.timer.set_timer(time.time(), 8)
                    return True
        return False

    # Decide which animation can be show now, depends of time and light level
    def get_sensors_status(self, actual_motion_status, actual_light_status):
        if not self.timer.check_statement():  # day time
            if self.timer.get_wake_up():  # if changed from night to day
                return 5
            if self.get_dusk_status(actual_light_status):  # dark
                if not self.timer.get_blocked():  # can start new animation
                    if self.status.motionSensorController.check_if_triggered():  # somebody triggered animation
                        self.status.animationOnProgress = True
                        return 2
                    else:  # nobody triggered
                        self.status.animationOnProgress = False
                        return 3
                else:  # animation is on going
                    self.status.animationOnProgress = True
                    return 2
            else:  # brightly
                self.timer.check_timer(time.time(), actual_motion_status)
        else:  # night time
            if self.looking_for_motion(actual_motion_status, actual_light_status):  # somebody triggered animation
                self.status.animationOnProgress = True
                return 4
            else:  # nobody triggered
                self.timer.check_timer(time.time(), actual_motion_status)
                if self.timer.get_unblocked():  # clear LED's because nobody is here
                    self.status.animationOnProgress = True
                    return 1
        return -1

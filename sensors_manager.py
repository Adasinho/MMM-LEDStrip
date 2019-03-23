# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from status import *
from timer import *

import time

USE_DUSK_DETECTOR = True


class SensorsManager:
    def __init__(self, actual_motion_status, actual_light_status):
        self.timer = Timer()
        self.status = Status(actual_motion_status, True)
        self.last_light_status = actual_light_status  # False - day, True - night

    # If use dusk detector, then return True if we have night or False when day
    def get_dusk_status(self, actual_light):
        if USE_DUSK_DETECTOR:
            actual_light_status = actual_light
            if actual_light_status != self.last_light_status:
                self.last_light_status = actual_light_status
            return actual_light_status
        else:
            return True

    def looking_for_motion(self, actual_motion_status, actual_light_status):
        self.timer.check_timer(time.time(), actual_motion_status)
        if not self.timer.get_blocked():
            if self.status.led_mode == 0:
                # If can't animate
                if not self.status.checkpoint(actual_motion_status, self.get_dusk_status(actual_light_status)):
                    self.timer.set_timer(time.time(), 8)
                    return True
        return False

    # Decide which animation can be show now, depends of time and light level
    def check_status(self, actual_light_status):
        actual_light_lvl = self.get_dusk_status(actual_light_status)

        if not self.timer.sleep_time():
            if self.timer.get_wake_up():
                return 1
            # when we have dark
            if actual_light_lvl:
                if not self.timer.get_blocked():
                    if self.status.get_motion_trigger():
                        self.status.led_mode = 1
                        return 2
                    else:
                        self.status.led_mode = 0
                        return 3
                else:
                    self.status.led_mode = 1
                    return 2
        else:
            if self.status.get_motion_trigger():
                if not self.timer.get_blocked():
                    self.timer.set_timer(time.time(), 10)
                    self.status.led_mode = 0
                    return 4
            else:
                return 1
        return -1

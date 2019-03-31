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
    def check_status(self, actual_motion_status, actual_light_status):

        # day time
        if not self.timer.sleep_time():
            if self.timer.get_wake_up():
                return 5
            dark = self.get_dusk_status(actual_light_status)
            # when we have dark
            if dark:
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
                self.timer.check_timer(time.time(), actual_motion_status)
        else:
            if self.looking_for_motion(actual_motion_status, actual_light_status):
                self.status.led_mode = 1
                return 4
            else:
                self.timer.check_timer(time.time(), actual_motion_status)
                if self.timer.get_unblocked():
                    self.status.led_mode = 1
                    return 1
        return -1

# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from status import *
from timer import *

import shared_variables
import time


class AnimationController:
    def __init__(self):
        self.timer = Timer()
        self.status = Status()
        self.animationOnProgress = False

    def looking_for_motion(self):
        self.timer.check_timer(time.time(), self.status.motionSensorController.get_motion_status())
        if not self.timer.get_blocked():
            if not self.animationOnProgress:
                # If can't animate
                if not self.status.checkpoint():
                    self.timer.set_timer(time.time(), 8)
                    return True
        return False

    # Decide which animation can be show now, depends of time and light level
    def get_animation(self):
        if not self.timer.check_statement():  # day time
            if self.timer.get_wake_up():  # if changed from night to day
                return 5
            if self.status.duskSensorController.get_dusk_status():  # dark
                if not self.timer.get_blocked():  # can start new animation
                    if self.status.motionSensorController.check_if_triggered():  # somebody triggered animation
                        self.animationOnProgress = True
                        return 2
                    else:  # nobody triggered
                        self.animationOnProgress = False
                        return 3
                else:  # animation is on going
                    self.animationOnProgress = True
                    return 2
            else:  # brightly
                self.timer.check_timer(time.time(), self.status.motionSensorController.get_motion_status())
        else:  # night time
            if self.looking_for_motion():  # somebody triggered animation
                self.animationOnProgress = True
                return 4
            else:  # nobody triggered
                self.timer.check_timer(time.time(), self.status.motionSensorController.get_motion_status())
                if self.timer.get_unblocked():  # clear LED's because nobody is here
                    self.animationOnProgress = True
                    return 1
        return -1

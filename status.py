# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

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

    def checkpoint(self, actual_motion_status, actual_light_level):
        if actual_light_level:
            if not self.check_motion(actual_motion_status):  # When nobody is move
                return True  # Can animate

        return False  # Can't animate
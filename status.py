# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)


# Class to control LEDs
class Status:
    def __init__(self, actual_light_lvl):
        self.lightLvl = actual_light_lvl
        self.animationOnProgress = False

        import motion_sensor_controller
        self.motionSensorController = motion_sensor_controller.MotionSensorController()

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

    def checkpoint(self, actual_motion_status, actual_light_level):
        self.motionSensorController.update()
        if actual_light_level:  # If dark
            if not self.motionSensorController.get_motion_status():  # When nobody is move
                return True  # Can animate
        return False  # Can't animate

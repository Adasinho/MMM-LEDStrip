# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

import motion_sensor_controller
import dusk_sensor_controller


# Class to control LEDs
class Status:
    def __init__(self):
        self.motionSensorController = motion_sensor_controller.MotionSensorController()
        self.duskSensorController = dusk_sensor_controller.DuskSensorController()

    def checkpoint(self):
        self.motionSensorController.update()
        self.duskSensorController.update()
        if self.duskSensorController.get_light_status():  # If dark
            if not self.motionSensorController.get_motion_status():  # When nobody is move
                return True  # Can animate
        return False  # Can't animate

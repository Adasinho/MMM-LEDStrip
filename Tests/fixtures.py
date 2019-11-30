from status import Status
from motion_sensor_controller import MotionSensorController
from dusk_sensor_controller import DuskSensorController
from animation_controller import AnimationController
from timer import Timer


class SensorsGetterFixture():
    def __init__(self, motion, light):
        self.motion_status = motion
        self.light_status = light

    def get_actual_motion_status(self):
        return self.motion_status

    def get_actual_light_status(self):
        return self.light_status

    def set_motion_status(self, new_motion_status):
        self.motion_status = new_motion_status

    def set_light_status(self, new_light_status):
        self.light_status = new_light_status


class DuckSensorControllerFixture(DuskSensorController):
    def __init__(self, sensors_getter):
        self.light_status = False
        self.triggered = False
        self.__sensors = sensors_getter.get_actual_light_status()

    def get_dusk_status(self):
        return self.__sensors


class MotionSensorControllerFixture(MotionSensorController):
    def __init__(self, sensors_getter):
        self.motionStatus = False
        self.triggered = False
        self.__sensors = sensors_getter

    def get_motion_status(self):
        return self.__sensors.get_actual_motion_status()


class StatusFixture(Status):
    def __init__(self, actual_light_lvl, sensors_getter):
        self.lightLvl = actual_light_lvl
        self.motionSensorController = MotionSensorControllerFixture(sensors_getter)
        self.duskSensorController = DuckSensorControllerFixture(sensors_getter)


class AnimationControllerFixture(AnimationController):
    def __init__(self, actual_light_status, sensors_getter):
        self.timer = Timer()
        self.status = StatusFixture(True, sensors_getter)
        self.last_light_status = actual_light_status
        self.animationOnProgress = False


class TestFixture():
    def __init__(self, motion_status, light_status):
        self.actual_motion_status = motion_status
        self.actual_light_status = light_status

        self.sensors_getter = SensorsGetterFixture(motion_status, light_status)
        self.manager = AnimationControllerFixture(self.actual_light_status, self.sensors_getter)

    def set_motion_status(self, motion_status):
        self.actual_motion_status = motion_status
        self.sensors_getter.set_motion_status(motion_status)

    def set_light_status(self, light_status):
        self.actual_light_status = light_status
        self.sensors_getter.set_light_status(light_status)

    def set_motion_and_light_status(self, motion_status, light_status):
        self.actual_light_status = light_status
        self.actual_motion_status = motion_status

    def get_dusk_status(self):
        return self.manager.status.duskSensorController.get_dusk_status()

    def get_looking_for_motion(self):
        return self.manager.looking_for_motion()

    def get_check_status(self):
        return self.manager.get_animation()

    def checkpoint(self):
        self.manager.status.checkpoint()
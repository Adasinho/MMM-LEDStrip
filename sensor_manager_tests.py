from sensors_manager import SensorsManager
from timer import *

import unittest


class MyTestCase(unittest.TestCase):
    def test_givenGetDuskStatusWhenMotionAndLightIsFalseThenShouldReturnedFalse(self):
        actual_motion_status = False
        actual_light_status = False
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(False, manager.get_dusk_status(actual_light_status))

    def test_givenGetDuskStatusWhenMotionIsTrueAndLightIsFalseThenShouldReturnedFalse(self):
        actual_motion_status = True
        actual_light_status = False
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(False, manager.get_dusk_status(actual_light_status))

    def test_givenGetDuskStatusWhenMotionIsFalseAndLightIsTrueThenShouldReturnedFalse(self):
        actual_motion_status = False
        actual_light_status = True
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(True, manager.get_dusk_status(actual_light_status))

    def test_givenGetDuskStatusWhenMotionAndLightIsTrueThenShouldReturnedFalse(self):
        actual_motion_status = True
        actual_light_status = True
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(True, manager.get_dusk_status(actual_light_status))

    def test_givenLookingForMotionWhenTimerIsBlockedThenReturnTrue(self):
        actual_motion_status = True
        actual_light_status = True      # Night time
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(True, manager.looking_for_motion(actual_motion_status, actual_light_status))
        self.assertEqual(True, manager.timer.get_blocked())

    def test_givenLookingForMotionWhenTimerIsUnlockedThenReturnFalse(self):
        actual_motion_status = False
        actual_light_status = True  # Night time
        manager = SensorsManager(actual_motion_status, actual_light_status)

        actual_motion_status = True
        manager.looking_for_motion(actual_motion_status, actual_light_status)
        actual_motion_status = False
        manager.timer.lastTime -= 9

        self.assertEqual(False, manager.looking_for_motion(actual_motion_status, actual_light_status))
        self.assertEqual(False, manager.timer.get_blocked())

    def test_givenCheckStatusWhenLightIsFalseThenReturnOffAnimationMode(self):
        actual_motion_status = False    # Nobody here
        actual_light_status = False     # Day time
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(-1, manager.check_status(actual_motion_status, actual_light_status))  # -1 means, turn off animations

    def test_givenCheckStatusWhenLightIsTrueAndTimerIsUnlockedThenReturnIdleAnimationMode(self):
        actual_motion_status = False  # Nobody here
        actual_light_status = True  # Night time
        custom_night_hours(-1, 25)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(3, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenCheckStatusWhenWeHaveNightAndSomebodyIsNearMirrorThenReturnTriggerAnimationMode(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(-1, 25)
        manager = SensorsManager(actual_motion_status, actual_light_status)
        actual_motion_status = True
        manager.status.checkpoint(actual_motion_status, actual_light_status)

        self.assertEqual(2, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenCheckStatusWhenWeHaveNightAndSomebodyIsNearMirrorThenReturnAnimationMode(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(-1, 25)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(3, manager.check_status(actual_motion_status, actual_light_status))
        actual_motion_status = True
        manager.looking_for_motion(actual_motion_status, actual_light_status)
        self.assertEqual(2, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenCheckStatusWhenNightTimeIsEndedThenReturnOffAnimationMode(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(25, -1)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        manager.check_status(actual_motion_status, actual_light_status)
        custom_night_hours(-1, 25)
        self.assertEqual(1, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenCheckStatusWhenSomebodyIsNearMirrorAtSleepTimeThenReturnSleepAnimationMode(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(25, -1)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        actual_motion_status = True
        self.assertEqual(4, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenCheckStatusWhenSomebodyGoOutAtSleepTimeThenAfterTenSecondsReturnOffAnimationMode(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(25, -1)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        actual_motion_status = True
        manager.check_status(actual_motion_status, actual_light_status)
        actual_motion_status = False

        manager.timer.lastTime -= 11
        self.assertEqual(1, manager.check_status(actual_motion_status, actual_light_status))
        self.assertEqual(-1, manager.check_status(actual_motion_status, actual_light_status))

    def test_givenSleepTimeWhenIsTimeToSleepThenReturnTrue(self):
        actual_motion_status = False
        actual_light_status = True
        custom_night_hours(-1, 25)
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(False, manager.timer.sleep_time())
        custom_night_hours(25, -1)
        self.assertEqual(True, manager.timer.sleep_time())


if __name__ == '__main__':
    unittest.main()

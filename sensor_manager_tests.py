from Tests.fixtures import *
from timer import *

import unittest


class MyTestCase(unittest.TestCase):
    def test_givenGetDuskStatusWhenMotionAndLightIsFalseThenShouldReturnedFalse(self):
        manager_fixture = TestFixture(False, False)  # Nobody here, Day time

        self.assertEqual(False, manager_fixture.get_dusk_status())

    def test_givenGetDuskStatusWhenMotionIsTrueAndLightIsFalseThenShouldReturnedFalse(self):
        manager_fixture = TestFixture(True, False)  # Somebody here, Day time

        self.assertEqual(False, manager_fixture.get_dusk_status())

    def test_givenGetDuskStatusWhenMotionIsFalseAndLightIsTrueThenShouldReturnedTrue(self):
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        self.assertEqual(True, manager_fixture.get_dusk_status())

    def test_givenGetDuskStatusWhenMotionAndLightIsTrueThenShouldReturnedTrue(self):
        manager_fixture = TestFixture(True, True)  # Somebody here, Night time

        self.assertEqual(True, manager_fixture.get_dusk_status())

    def test_givenLookingForMotionWhenTimerIsBlockedThenReturnTrue(self):
        manager_fixture = TestFixture(True, True)  # Somebody here, Night time

        self.assertEqual(True, manager_fixture.get_looking_for_motion())
        self.assertEqual(True, manager_fixture.manager.timer.get_blocked())

    def test_givenLookingForMotionWhenTimerIsUnlockedThenReturnFalse(self):
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        manager_fixture.set_motion_status(True)
        manager_fixture.get_looking_for_motion()
        manager_fixture.set_motion_status(False)
        manager_fixture.manager.timer.lastTime -= 9

        self.assertEqual(False, manager_fixture.get_looking_for_motion())
        self.assertEqual(False, manager_fixture.manager.timer.get_blocked())

    def test_givenCheckStatusWhenLightIsFalseThenReturnOffAnimationMode(self):
        custom_night_hours(-1, 25)
        manager_fixture = TestFixture(False, False)  # Nobody here, Day time

        self.assertEqual(-1, manager_fixture.get_check_status())  # -1 means, turn off animations

    def test_givenCheckStatusWhenLightIsTrueAndTimerIsUnlockedThenReturnIdleAnimationMode(self):
        custom_night_hours(-1, 25)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        self.assertEqual(3, manager_fixture.get_check_status())

    def test_givenCheckStatusWhenWeHaveNightAndSomebodyIsNearMirrorThenReturnTriggerAnimationMode(self):
        custom_night_hours(-1, 25)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time
        manager_fixture.set_motion_status(True)
        manager_fixture.checkpoint()

        self.assertEqual(2, manager_fixture.get_check_status())

    def test_givenCheckStatusWhenWeHaveNightAndSomebodyIsNearMirrorThenReturnAnimationMode(self):
        custom_night_hours(-1, 25)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        self.assertEqual(3, manager_fixture.get_check_status())
        manager_fixture.set_motion_status(True)
        manager_fixture.get_looking_for_motion()
        self.assertEqual(2, manager_fixture.get_check_status())

    def test_givenCheckStatusWhenNightTimeIsEndedThenReturnOffAnimationMode(self):
        custom_night_hours(25, -1)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        manager_fixture.get_check_status()
        custom_night_hours(-1, 25)
        self.assertEqual(5, manager_fixture.get_check_status())

    def test_givenCheckStatusWhenSomebodyIsNearMirrorAtSleepTimeThenReturnSleepAnimationMode(self):
        custom_night_hours(25, -1)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        manager_fixture.set_motion_status(True)
        self.assertEqual(4, manager_fixture.get_check_status())

    def test_givenCheckStatusWhenSomebodyGoOutAtSleepTimeThenAfterTenSecondsReturnOffAnimationMode(self):
        custom_night_hours(25, -1)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        manager_fixture.set_motion_status(True)
        manager_fixture.get_check_status()
        manager_fixture.set_motion_status(False)

        manager_fixture.manager.timer.lastTime -= 11
        self.assertEqual(1, manager_fixture.get_check_status())
        self.assertEqual(-1, manager_fixture.get_check_status())

    def test_givenSleepTimeWhenIsTimeToSleepThenReturnTrue(self):
        custom_night_hours(-1, 25)
        manager_fixture = TestFixture(False, True)  # Nobody here, Night time

        self.assertEqual(False, manager_fixture.manager.timer.check_statement())
        custom_night_hours(25, -1)
        self.assertEqual(True, manager_fixture.manager.timer.check_statement())


if __name__ == '__main__':
    unittest.main()

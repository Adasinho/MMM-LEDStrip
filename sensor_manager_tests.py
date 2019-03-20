from sensors_manager import SensorsManager

import unittest


class MyTestCase(unittest.TestCase):
    def test_something(self):
        actual_motion_status = False
        actual_light_status = False
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(manager.get_dusk_status(actual_light_status), False)

    def test_something_1(self):
        actual_motion_status = False    # Nobody here
        actual_light_status = False     # Day time
        manager = SensorsManager(actual_motion_status, actual_light_status)

        self.assertEqual(manager.check_status(actual_light_status), -1)


if __name__ == '__main__':
    unittest.main()

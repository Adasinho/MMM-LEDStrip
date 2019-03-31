# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

import datetime

MORNING_HOUR = 6
NIGHT_HOUR = 23


class Timer:
    def __init__(self):
        self.blocked = False
        self.lastTime = 0
        self.duration = 0
        self.last_sleep_statement = False
        self.wake_up = False
        self.unblocked = False

    def check_timer(self, actual_time, motion):
        #print('Actual Time in ms: ', actual_time)
        #print('Last time + delay: ', self.lastTime + self.duration)
        if self.blocked:
            if (self.lastTime + self.duration) < actual_time:
                self.blocked = False
                self.unblocked = True
                print("Odblokowano")
            elif motion:
                self.set_timer(actual_time, 8)

    def set_timer(self, actual_time, how_long):
        self.lastTime = actual_time
        self.duration = how_long
        self.blocked = True

    def get_blocked(self):
        return self.blocked

    # Time when all LEDs are off (between night and morning)
    def sleep_time(self):
        now = datetime.datetime.now()
        if (now.hour > MORNING_HOUR) and (now.hour < NIGHT_HOUR):
            ret = False  # LEDs can animate
        else:
            ret = True  # LEDs can't animate, time to sleep!

        if self.last_sleep_statement != ret:
            self.last_sleep_statement = ret
            if not ret:
                self.wake_up = True

        return ret

    def get_wake_up(self):
        if self.wake_up:
            self.wake_up = False
            return True
        else:
            return False

    def get_unblocked(self):
        if self.unblocked:
            self.unblocked = False
            return True
        return False


def custom_night_hours(morning_hour, night_hour):
    global MORNING_HOUR, NIGHT_HOUR

    MORNING_HOUR = morning_hour
    NIGHT_HOUR = night_hour

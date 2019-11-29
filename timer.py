# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

import datetime
import shared_variables


class Timer:
    def __init__(self):
        self.startTimer = False
        self.endTimer = False
        self.lastTime = 0
        self.duration = 0
        self.lastStatement = False
        self.wakeUp = False

    def check_timer(self, actual_time, motion):
        #print('Actual Time in ms: ', actual_time)
        #print('Last time + delay: ', self.lastTime + self.duration)
        if self.startTimer:
            if (self.lastTime + self.duration) < actual_time:
                self.startTimer = False
                self.endTimer = True
                print("Odblokowano")
            elif motion:
                self.set_timer(actual_time, 8)

    def set_timer(self, actual_time, how_long):
        self.lastTime = actual_time
        self.duration = how_long
        self.startTimer = True

    def get_blocked(self):
        return self.startTimer

    # Time when all LEDs are off (between night and morning)
    def check_statement(self):
        now = datetime.datetime.now()
        if (now.hour > shared_variables.MORNING_HOUR) and (now.hour < shared_variables.NIGHT_HOUR):
            ret = False  # LEDs can animate
        else:
            ret = True  # LEDs can't animate, time to sleep!

        if self.lastStatement != ret:
            self.lastStatement = ret
            if not ret:
                self.wakeUp = True

        return ret

    def get_wake_up(self):
        if self.wakeUp:
            self.wakeUp = False
            return True
        else:
            return False

    def get_unblocked(self):
        if self.endTimer:
            self.endTimer = False
            return True
        return False


def custom_night_hours(morning_hour, night_hour):
    shared_variables.MORNING_HOUR = morning_hour
    shared_variables.NIGHT_HOUR = night_hour

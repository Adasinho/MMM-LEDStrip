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

    def check_timer(self, actual_time, motion):
        print 'Actual Time in ms: ', actual_time
        print 'Last time + delay: ', self.lastTime + self.duration
        if self.blocked:
            if (self.lastTime + self.duration) < actual_time:
                self.blocked = False
            elif motion:
                self.set_timer(actual_time, 8)

    def set_timer(self, actual_time, how_long):
        self.lastTime = actual_time
        self.duration = how_long
        self.blocked = True

    def get_blocked(self):
        return self.blocked

# Time when all leds are off (between night and morning)
def sleep_time():
    now = datetime.datetime.now()
    if (now.hour > MORNING_HOUR) and (now.hour < NIGHT_HOUR):
        return False # LEDs can animate
    else:
        return True # LEDs can't animate, time to sleep!
from shared_variables import *

import RPi.GPIO as GPIO


def get_actual_motion_status():
    return GPIO.input(GPiO_MOTION_SENSOR)


def get_actual_light_status():
    return GPIO.input(GPiO_LIGHT_SENSOR)

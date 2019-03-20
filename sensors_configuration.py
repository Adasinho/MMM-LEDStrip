import RPi.GPIO as GPIO

GPIO_MOTION_SENSOR = 11
GPIO_LIGHT_SENSOR = 13


def get_actual_motion_status():
    return GPIO.input(GPIO_MOTION_SENSOR)


def get_actual_light_status():
    return GPIO.input(GPIO_LIGHT_SENSOR)


def init():
    # Initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(GPIO_MOTION_SENSOR, GPIO.IN)
    GPIO.setup(GPIO_LIGHT_SENSOR, GPIO.IN)

# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from neopixel import *
from animations import dynamic_breath, idle_animation, mirror_fall, fade_out_from_current_brightness_no_trigger, fade_out
from sensors_manager import SensorsManager
from sensors_configuration import *

import argparse

# LED strip configuration dynamic_breath:
LED_COUNT = 116  # Number of LED pixels
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!)
LED_FREQ_HZ = 800000  # LED sugbak frequency in hertz (usually 800 khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


def update():
    ref = manager.check_status(get_actual_motion_status(), get_actual_light_status())
    if ref == 2:
        dynamic_breath(strip, manager)
    elif ref == 3:
        idle_animation(strip, manager)
    elif ref == 4:
        mirror_fall(strip, Color(250, 255, 205), 47, 69)
    elif ref == 5:
        manager.status.led_mode = 0
        strip.setBrightness(255)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 255, 255))
    elif ref == 1:
        fade_out_from_current_brightness_no_trigger(strip, manager)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # init GPIO
    init()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    # Initialize Sensors Manager
    manager = SensorsManager(get_actual_motion_status(), get_actual_light_status())

    print ('Press Crtl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    manager.status.led_mode = 1  # 0 - idle mode, 1 - trigger mode

    mirror_fall(strip, Color(99, 255, 71), 0, LED_COUNT)  # First welcome animate
    fade_out(strip, manager)

    try:
        while True:
            update()

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)

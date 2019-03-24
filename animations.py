# Custom magicmirror effects with NeoPixel library
# Author: Adasinho (adirm10@yahoo.com)

from neopixel import *
from sensors_configuration import *
from random import randint

import time

colors = [Color(99, 255, 71), Color(255, 127, 0), Color(144, 30, 255), Color(0, 148, 211), Color(250, 255, 205), Color(222, 255, 173)]
last_color_choose = 0


def un_color(color):
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


def fade_in(led_strip, manager, color, wait_ms=10):
    for i in range(255):
        for k in range(led_strip.numPixels()):
            led_strip.setPixelColor(k, color)
        led_strip.setBrightness(i)
        led_strip.show()
        if manager.looking_for_motion(get_actual_motion_status(), get_actual_light_status()):
            dynamic_breath(led_strip, manager)
            return False
        time.sleep(wait_ms / 1000.0)
    return True


def fade_out(led_strip, manager, wait_ms=10):
    for i in range(255, 0, -1):
        led_strip.setBrightness(i)
        led_strip.show()
        if manager.looking_for_motion(get_actual_motion_status(), get_actual_light_status()):
            dynamic_breath(led_strip, manager)
            return False
        time.sleep(wait_ms / 1000.0)
    turn_off_led_strip(led_strip)
    return True


# Smooth transition form old color to new
def smooth_color_transition(led_strip, manager, new_color, wait_ms=20):
    if led_strip.getBrightness() != 120:
        dynamic_breath(led_strip, manager, 120)

    old_color = un_color(led_strip.getPixelColor(0))
    r = old_color[0]
    g = old_color[1]
    b = old_color[2]
    direction = [1, 1, 1]
    max = 0

    temp_new_color = un_color(new_color)

    if r > temp_new_color[0]:
        direction[0] = -1
    tmp = abs(r - temp_new_color[0])
    if tmp > max:
        max = tmp
    if g > temp_new_color[1]:
        direction[1] = -1
    tmp = abs(g - temp_new_color[1])
    if tmp > max:
        max = tmp
    if b > temp_new_color[2]:
        direction[2] = -1
    tmp = abs(b - temp_new_color[2])
    if tmp > max:
        max = tmp

    for i in range(max):
        if r != temp_new_color[0]:
            r = r + direction[0]
        if g != temp_new_color[1]:
            g = g + direction[1]
        if b != temp_new_color[2]:
            b = b + direction[2]

        old_color = Color(r, g, b)

        for k in range(led_strip.numPixels()):
            led_strip.setPixelColor(k, old_color)
        led_strip.show()
        if manager.looking_for_motion(get_actual_motion_status(), get_actual_light_status()):
            dynamic_breath(led_strip, manager)
            return False
        time.sleep(wait_ms / 1000.0)


# Animation when somebody is near mirror
def dynamic_breath(led_strip, manager, to_brightness=0):
    if to_brightness != 0:
        new_brightness = to_brightness
    else:
        if randint(0, 1) == 0:
            new_brightness = randint(30, 100)
        else:
            new_brightness = randint(165, 235)

    direction = 1
    old_brightness = led_strip.getBrightness()
    if old_brightness < new_brightness:
        animation_range = abs(old_brightness - new_brightness)
    else:
        direction = -1
        animation_range = abs(old_brightness - new_brightness)

    for i in range(animation_range):
        old_brightness = old_brightness + direction
        led_strip.setBrightness(old_brightness)
        led_strip.show()
        time.sleep(5 / 1000.0)

    manager.timer.check_timer(time.time(), get_actual_motion_status())
    if not manager.timer.get_blocked():
        manager.status.led_mode = 0


# turn off leds
def turn_off_led_strip(led_strip):
    for i in range(led_strip.numPixels()):
        led_strip.setPixelColor(i, Color(0, 0, 0))
    led_strip.setBrightness(0)
    led_strip.show()


# Animation when nobody is near mirror
def idle_animation(led_strip, manager):
    while True:
        tmp = randint(0, 5)
        if tmp != last_color_choose:
            smooth_color_transition(led_strip, manager, colors[tmp])
            return True


# Animation effect
def snake(led_strip, length, wait_ms=5):
    temp_color = 0
    for i in range(led_strip.numPixels()):
        if (i + length) < led_strip.numPixels():
            temp_color = led_strip.getPixelColor(i)
            led_strip.setPixelColor(i + length, temp_color)
        else:
            temp_color = led_strip.getPixelColor(i)
            led_strip.setPixelColor(i + length - led_strip.numPixels(), temp_color)
        led_strip.setPixelColor(i, Color(0, 0, 0))
        led_strip.show()
        time.sleep(wait_ms / 1000.0)
    led_strip.setPixelColor(length, temp_color)
    led_strip.show()
    time.sleep(wait_ms / 1000.0)


# Animation effect
def loading(led_strip, color, length, speed=10.0):
    turn_off_led_strip(led_strip)
    led_strip.setBrightness(255)
    for i in range(length):
        led_strip.setPixelColor(i, color)

    for i in range(length, led_strip.numPixels(), 1):
        led_strip.setPixelColor(i, color)
        if i % 10 == 0:
            speed = float(speed / 2.0)
        snake(led_strip, i, speed)


# Animation effect
def water_fall(led_strip, status, wait_ms=50):  # Trigger animation
    """Waterfall"""
    turn_off_led_strip(led_strip)
    led_strip.setBrightness(255)
    led_strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))

    temp_color = 0
    for i in range(led_strip.numPixels()):
        for k in range(i, 0, -1):
            temp_color = led_strip.getPixelColor(k - 1)
            led_strip.setPixelColor(k, temp_color)
        led_strip.setPixelColor(0, Color(0, randint(0, 127), randint(0, 255)))
        led_strip.show()
        time.sleep(wait_ms / 1000.0)
    status.led_mode = 0


def fade_out_from_current_brightness(led_strip, manager, wait_ms=10):
    for i in range(led_strip.getBrightness(), 0, -1):
        led_strip.setBrightness(i)
        led_strip.show()
        if manager.looking_for_motion(get_actual_motion_status(), get_actual_light_status()):
            dynamic_breath(led_strip, manager)
            return False
        time.sleep(wait_ms / 1000.0)
    return True


def fade_out_from_current_brightness_no_trigger(led_strip, wait_ms=10):
    for i in range(led_strip.getBrightness(), 0, -1):
        led_strip.setBrightness(i)
        led_strip.show()
        time.sleep(wait_ms / 1000.0)
    turn_off_led_strip(led_strip)


# Animation effect
def rooling(led_strip, manager, wait_ms=20):
    for i in range(led_strip.numPixels() - 1, 1, -1):
        tmp = led_strip.getPixelColor(i - 1)
        led_strip.setPixelColor(i - 1, led_strip.getPixelColor(i))
        led_strip.setPixelColor(i, tmp)
    tmp = led_strip.getPixelColor(0)
    led_strip.setPixelColor(0, led_strip.getPixelColor(led_strip.numPixels() - 1))
    led_strip.setPixelColor(led_strip.numPixels() - 1, tmp)

    led_strip.show()
    time.sleep(wait_ms / 1000.0)

    manager.timer.check_timer(time.time(), get_actual_motion_status())
    if not manager.timer.get_blocked():
        manager.status.led_mode = 0
        fade_out(led_strip, manager)


# Animation effect
def breath(led_strip, manager, color, wait_ms=10):  # idle animation
    """Breath effect"""

    turn_off_led_strip(led_strip)

    if not fade_in(led_strip, manager, color):
        return False
    if not fade_out(led_strip, manager):
        return False

    turn_off_led_strip(led_strip)
    time.sleep(0.2)


# Animation effect
def mirror_fall(led_strip, color, start_led, stop_led, wait_ms=50):
    """Mirror Fall"""

    led_strip.setBrightness(255)

    led_quantity = stop_led - start_led

    if led_quantity % 2 == 0:
        x1 = start_led + (led_quantity / 2) - 1
        x2 = start_led + (led_quantity / 2)
        iterations = led_quantity / 2 - 1
    else:
        x1 = start_led + (led_quantity / 2)
        x2 = start_led + (led_quantity / 2)
        iterations = led_quantity / 2 + 1

    for i in range(iterations):
        led_strip.setPixelColor(x1 - i, color)
        led_strip.setPixelColor(x2 + i, color)
        led_strip.show()
        time.sleep(wait_ms / 1000.0)

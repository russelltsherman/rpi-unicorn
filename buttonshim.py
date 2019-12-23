#!/usr/bin/env python3

import signal
import buttonshim
import os

print("""
Button SHIM: rainbow.py
Light up the LED a different colour of the rainbow with each button pressed.
Press Ctrl+C to exit.
""")


@buttonshim.on_press(buttonshim.BUTTON_A)
def button_a(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False
    buttonshim.set_pixel(0x94, 0x00, 0xd3)

@buttonshim.on_release(buttonshim.BUTTON_A)
def release_handler(button, pressed):
    global button_was_held
    if not button_was_held:
        os.system('/home/pi/rpi-unicorn-phat/examples/binary_clock.py')

@buttonshim.on_press(buttonshim.BUTTON_B)
def button_b(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False
    buttonshim.set_pixel(0x00, 0x00, 0xff)

@buttonshim.on_release(buttonshim.BUTTON_B)
def release_handler(button, pressed):
    global button_was_held
    if not button_was_held:
        os.system('/home/pi/rpi-unicorn-phat/examples/demo.py')

@buttonshim.on_press(buttonshim.BUTTON_C)
def button_c(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False
    buttonshim.set_pixel(0x00, 0xff, 0x00)

@buttonshim.on_release(buttonshim.BUTTON_C)
def release_handler(button, pressed):
    global button_was_held
    if not button_was_held:
        os.system('/home/pi/rpi-unicorn-phat/examples/random_blinky.py')

@buttonshim.on_press(buttonshim.BUTTON_D)
def button_d(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False
    buttonshim.set_pixel(0xff, 0xff, 0x00)

@buttonshim.on_release(buttonshim.BUTTON_D)
def release_handler(button, pressed):
    global button_was_held
    if not button_was_held:
        os.system('/home/pi/rpi-unicorn-phat/examples/random_sparkles.py')

@buttonshim.on_press(buttonshim.BUTTON_E)
def button_e(button, pressed):
    global button_was_held    # So we change the global var defined above
    button_was_held = False
    buttonshim.set_pixel(0xff, 0x00, 0x00)

@buttonshim.on_release(buttonshim.BUTTON_E)
def release_handler(button, pressed):
    global button_was_held
    if not button_was_held:
        os.system('/home/pi/rpi-unicorn-phat/examples/snowy.py')


signal.pause()
#!/usr/bin/env python3

import adafruit_platformdetect

detect = adafruit_platformdetect.PlatformDetect()

print("Chip name: ", detect.chip.name)

print("Board name: ", detect.board.name)

if detect.board.any_raspberry_pi:
    print("Raspberry Pi detected.")
    print("Revision code: ", detect.board.pi_rev_code)

if detect.board.beaglebone_black:
    print("BBB detected")

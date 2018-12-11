#!/usr/bin/env python3

import adafruit_platformdetect

detect = adafruit_platformdetect.PlatformDetect()

print("Chip id: ", detect.chip.id)

print("Board id: ", detect.board.id)

print("Is this a Pi 3B+?", detect.board.RASPBERRY_PI_3B_PLUS)
print("Is this a BBB?", detect.board.BEAGLEBONE_BLACK)

if detect.board.any_raspberry_pi:
    print("Raspberry Pi detected.")
    print("Revision code: ", detect.board._pi_rev_code())

if detect.board.beaglebone_black:
    print("BBB detected")

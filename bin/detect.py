#!/usr/bin/env python3

import adafruit_platformdetect

detector = adafruit_platformdetect.PlatformDetector()

print("Chip id: ", detector.chip.id)

print("Board id: ", detector.board.id)

print("Is this a Pi 3B+?", detector.board.RASPBERRY_PI_3B_PLUS)
print("Is this a BBB?", detector.board.BEAGLEBONE_BLACK)

if detector.board.any_raspberry_pi:
    print("Raspberry Pi detected.")
    print("Revision code: ", detector.board._pi_rev_code())

if detector.board.BEAGLEBONE_BLACK:
    print("BBB detected")

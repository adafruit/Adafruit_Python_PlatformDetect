#!/usr/bin/env python3

import adafruit_platformdetect

detector = adafruit_platformdetect.Detector()

print("Chip id: ", detector.chip.id)

print("Board id: ", detector.board.id)

print("Is this a Pi 3B+?", detector.board.RASPBERRY_PI_3B_PLUS)
print("Is this a BBB?", detector.board.BEAGLEBONE_BLACK)
print("Is this an Orange Pi PC?", detector.board.ORANGE_PI_PC)
print("Is this a generic Linux PC?", detector.board.GENERIC_LINUX_PC)

if detector.board.any_raspberry_pi:
    print("Raspberry Pi detected.")

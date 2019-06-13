#!/usr/bin/env python3

import adafruit_platformdetect

detector = adafruit_platformdetect.Detector()

print("Chip id: ", detector.chip.id)

print("Board id: ", detector.board.id)

print("Is this a 96Boards board?", detector.board.LINARO_96BOARDS)
print("Is this a Pi 3B+?", detector.board.RASPBERRY_PI_3B_PLUS)
print("Is this a 40-pin Raspberry Pi?", detector.board.any_raspberry_pi_40_pin)
print("Is this a BBB?", detector.board.BEAGLEBONE_BLACK)
print("Is this a Giant Board?", detector.board.GIANT_BOARD)
print("Is this a Coral Edge TPU?", detector.board.CORAL_EDGE_TPU_DEV)
print("Is this an embedded Linux system?", detector.board.any_embedded_linux)
print("Is this a generic Linux PC?", detector.board.GENERIC_LINUX_PC)

if detector.board.any_raspberry_pi:
    print("Raspberry Pi detected.")

if detector.board.any_jetson_board:
    print("Jetson platform detected.")

if detector.board.any_orange_pi:
    print("Orange Pi detected.")

if detector.board.any_odroid_40_pin:
    print("Odroid detected.")

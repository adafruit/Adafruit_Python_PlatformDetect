#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`bin.detect`
================================================================================

Board detection and determination script

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

"""

import adafruit_platformdetect

detector = adafruit_platformdetect.Detector()

print("Board Detection Test")
print()
print("Check that the Chip and Board IDs match your board and that this it is")
print("correctly detecting whether or not it is a Linux board.")
print()
print("Chip id: ", detector.chip.id)
print("Board id: ", detector.board.id)
print()
print("Linux Detection")
print("---------------")
print("Is this an embedded Linux system?", detector.board.any_embedded_linux)
print()
print("Raspberry Pi Boards")
print("-------------------")
if detector.board.any_raspberry_pi:
    print("Raspberry Pi detected.")
print("Is this a Pi 3B+?", detector.board.RASPBERRY_PI_3B_PLUS)
print("Is this a Pi 4B?", detector.board.RASPBERRY_PI_4B)
print("Is this a 40-pin Raspberry Pi?", detector.board.any_raspberry_pi_40_pin)
print("Is this a Raspberry Pi Compute Module?", detector.board.any_raspberry_pi_cm)
print()

print("Other Boards")
print("-------------------")
print(
    "Is this a Siemens Simatic IOT2000 Gateway?",
    detector.board.any_siemens_simatic_iot2000,
)
print("Is this a 96boards board?", detector.board.any_96boards)
print("Is this a BeagleBone board?", detector.board.any_beaglebone)
print("Is this a Giant board?", detector.board.any_giant_board)
print("Is this a Coral Dev board?", detector.board.any_coral_board)
print("Is this a MaaXBoard?", detector.board.any_maaxboard)
print("Is this a SiFive board? ", detector.board.any_sifive_board)
print("Is this a PYNQ board?", detector.board.any_pynq_board)
print("Is this a Rock Pi board?", detector.board.any_rock_pi_board)
print("Is this a NanoPi board?", detector.board.any_nanopi)
print("Is this a Khadas VIM3 board?", detector.board.khadas_vim3_40_pin)
print("Is this a Clockwork Pi board?", detector.board.any_clockwork_pi_board)
print("Is this a Seeed Board?", detector.board.any_seeed_board)
print("Is this a UDOO board?", detector.board.any_udoo_board)
print("Is this an ASUS Tinker board?", detector.board.any_asus_tinker_board)
print("Is this an STM32MP1 board?", detector.board.any_stm32mp1)
print("Is this a generic Linux PC?", detector.board.generic_linux)
print(
    "Is this an OS environment variable special case?", detector.board.os_environ_board
)

if detector.board.any_jetson_board:
    print("Jetson platform detected.")

if detector.board.any_tisk_board:
    print("TI platform detected.")

if detector.board.any_pynq_board:
    print("PYNQ platform detected.")

if detector.board.any_orange_pi:
    print("Orange Pi detected.")

if detector.board.any_odroid_40_pin:
    print("Odroid detected.")

if detector.board.any_onion_omega_board:
    print("Onion Omega detected.")

if detector.board.any_pine64_board:
    print("Pine64 device detected.")

if detector.board.any_rock_pi_board:
    print("Rock Pi device detected.")

if detector.board.any_clockwork_pi_board:
    print("Clockwork Pi device detected.")

if detector.board.any_asus_tinker_board:
    print("ASUS Tinker Board device detected.")

if detector.board.any_coral_board:
    print("Coral device detected.")

if detector.board.any_lubancat:
    print("LubanCat detected.")

if detector.board.any_siemens_simatic_iot2000:
    print("Siemens Simatic IOT2000 Gateway detected.")

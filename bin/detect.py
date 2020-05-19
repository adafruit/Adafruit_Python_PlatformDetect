#!/usr/bin/env python3

import adafruit_platformdetect

detector = adafruit_platformdetect.Detector()

print("Chip id: ", detector.chip.id)
print("Board id: ", detector.board.id)
print()

print("Is this a DragonBoard 410c?", detector.board.DRAGONBOARD_410C)
print("Is this a Pi 3B+?", detector.board.RASPBERRY_PI_3B_PLUS)
print("Is this a Pi 4B?", detector.board.RASPBERRY_PI_4B)
print("Is this a 40-pin Raspberry Pi?", detector.board.any_raspberry_pi_40_pin)
print("Is this a Raspberry Pi Compute Module?", detector.board.any_raspberry_pi_cm)
print("Is this a BeagleBone Black?", detector.board.BEAGLEBONE_BLACK)
print("Is this a BeagleBone Green?", detector.board.BEAGLEBONE_GREEN)
print("Is this a Giant Board?", detector.board.GIANT_BOARD)
print("Is this a Coral Edge TPU?", detector.board.CORAL_EDGE_TPU_DEV)
print("Is this a SiFive Unleashed? ", detector.board.SIFIVE_UNLEASHED)
print("Is this a PYNQ Board?", detector.board.PYNQ_Z1 | detector.board.PYNQ_Z2)
print("Is this a Rock Pi board?", detector.board.any_rock_pi_board)
print("Is this a Clockwork Pi board?", detector.board.any_clockwork_pi_board)
print("Is this an embedded Linux system?", detector.board.any_embedded_linux)
print("Is this a generic Linux PC?", detector.board.GENERIC_LINUX_PC)
print("Is this a UDOO Bolt?", detector.board.UDOO_BOLT)
print(
    "Is this an OS environment variable special case?",
    detector.board.FTDI_FT232H
    | detector.board.MICROCHIP_MCP2221
    | detector.board.BINHO_NOVA
    | detector.board.GREATFET_ONE,
)

if detector.board.any_raspberry_pi:
    print("Raspberry Pi detected.")

if detector.board.any_jetson_board:
    print("Jetson platform detected.")

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

if detector.board.any_clockwork_pi:
    print("Clockwork Pi device detected.")

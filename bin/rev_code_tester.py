#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`bin.rev_code_tester`
================================================================================

Tests that all existing rev codes in the boards constant file
 match what the decoder finds.

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

"""

import adafruit_platformdetect
import adafruit_platformdetect.constants.boards as ap_board
from adafruit_platformdetect.revcodes import PiDecoder

detector = adafruit_platformdetect.Detector()


def print_property(label, value):
    "Format and print a property"
    print(f"{label}: {value}")


def print_info(pi_decoder):
    "Print the info for the board"
    if pi_decoder.is_new_format():
        print_property("Overvoltage", pi_decoder.overvoltage)
        print_property("OTP Program", pi_decoder.otp_program)
        print_property("OTP Read", pi_decoder.otp_read)
        print_property("Warranty bit", pi_decoder.warranty_bit)
        print_property("New flag", pi_decoder.rev_style)
        print_property("Memory size", pi_decoder.memory_size)
        print_property("Manufacturer", pi_decoder.manufacturer)
        print_property("Processor", pi_decoder.processor)
        print_property("Type", pi_decoder.type)
        print_property("Revision", pi_decoder.revision)
    else:
        print_property("Warranty bit", pi_decoder.warranty_bit)
        print_property("Model", pi_decoder.type)
        print_property("Revision", pi_decoder.revision)
        print_property("RAM", pi_decoder.memory_size)
        print_property("Manufacturer", pi_decoder.manufacturer)


# Iterate through the _PI_REV_CODES dictionary to find the model
# Run the code through the decoder to check that:
#   - It is a valid code
#   - It matches the model
for model, codes in ap_board._PI_REV_CODES.items():  # pylint: disable=protected-access
    for pi_rev_code in codes:
        try:
            decoder = PiDecoder(pi_rev_code)
        except ValueError as e:
            print("Invalid revision code. It should be a hexadecimal value.")
        decoded_model = ap_board._PI_MODELS[  # pylint: disable=protected-access
            decoder.type_raw
        ]
        if isinstance(decoded_model, dict):
            decoded_model = decoded_model[decoder.revision]
        if decoded_model == model:
            print(f"Decoded model matches expected model: {model}")
        else:
            print(f"Decoded model does not match expected model: {model}")
            print(f"Decoded model: {decoded_model}")
            print(f"Expected model: {model}")
            print_info(decoder)

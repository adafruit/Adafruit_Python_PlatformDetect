# SPDX-FileCopyrightText: 2021-2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Identify specific models and revisions of Raspberry Pi boards."""
import re

import adafruit_platformdetect.constants.boards as board_ids
import adafruit_platformdetect.constants.chips as chips_ids

try:
    from typing import Optional, TYPE_CHECKING

    if TYPE_CHECKING:
        from adafruit_platformdetect import Detector
except ImportError:
    pass


# pylint: disable=protected-access
def determine_board_id(detector: "Detector") -> Optional[str]:
    """Try to detect id of a Raspberry Pi."""
    # Check for Pi boards:
    pi_rev_code = determine_rev_code(detector)
    if pi_rev_code:
        from adafruit_platformdetect.revcodes import PiDecoder

        try:
            decoder = PiDecoder(pi_rev_code)
            model = board_ids._PI_MODELS[decoder.type_raw]
            if isinstance(model, dict):
                model = model[decoder.revision]
            return model
        except ValueError:
            pass
    # We may be on a non-Raspbian OS, so try to lazily determine
    # the version based on `get_device_model`
    else:
        pi_model = detector.get_device_model()
        if pi_model:
            pi_model = pi_model.upper().replace(" ", "_")
            if "PLUS" in pi_model:
                re_model = re.search(r"(RASPBERRY_PI_\d).*([AB]_*)(PLUS)", pi_model)
            elif "CM" in pi_model:  # untested for Compute Module
                re_model = re.search(r"(RASPBERRY_PI_CM)(\d)", pi_model)
            else:  # untested for non-plus models
                re_model = re.search(r"(RASPBERRY_PI_\d).*([AB])", pi_model)

            if re_model:
                pi_model = "".join(re_model.groups())
                available_models = board_ids._PI_REV_CODES.keys()
                for model in available_models:
                    if model == pi_model:
                        return model

    return None


# pylint: enable=protected-access


def determine_rev_code(detector: "Detector") -> Optional[str]:
    """Attempt to find a Raspberry Pi revision code for this board."""
    # 2708 is Pi 1
    # 2709 is Pi 2
    # 2835 is Pi 3 (or greater) on 4.9.x kernel
    # Anything else is not a Pi.
    if detector.chip.id != chips_ids.BCM2XXX:
        # Something else, not a Pi.
        return None
    rev = detector.get_cpuinfo_field("Revision")

    if rev is not None:
        return rev

    try:
        with open("/proc/device-tree/system/linux,revision", "rb") as revision:
            rev_bytes = revision.read()

            if rev_bytes[:1] == b"\x00":
                rev_bytes = rev_bytes[1:]

            return rev_bytes.hex()
    except FileNotFoundError:
        return None

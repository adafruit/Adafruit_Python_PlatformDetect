import adafruit_platformdetect.chip as ap_chip
import platform
import sys
import re

# Pi revision codes from:
#   https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md

BEAGLEBONE_BLACK = "BEAGLEBONE_BLACK"
FEATHER_HUZZAH = "FEATHER_HUZZAH"
FEATHER_M0_EXPRESS="FEATHER_M0_EXPRESS"
PYBOARD = "PYBOARD"
NODEMCU = "NODEMCU"
ORANGE_PI_PC = "ORANGE_PI_PC"

RASPBERRY_PI_B = "RASPBERRY_PI_B"
RASPBERRY_PI_B_PLUS = "RASPBERRY_PI_B_PLUS"
RASPBERRY_PI_A = "RASPBERRY_PI_A"
RASPBERRY_PI_A_PLUS = "RASPBERRY_PI_A_PLUS"
RASPBERRY_PI_CM1 = "RASPBERRY_PI_CM1"
RASPBERRY_PI_ZERO = "RASPBERRY_PI_ZERO"
RASPBERRY_PI_ZERO_W = "RASPBERRY_PI_ZERO_W"
RASPBERRY_PI_2B = "RASPBERRY_PI_2B"
RASPBERRY_PI_3B = "RASPBERRY_PI_3B"
RASPBERRY_PI_3B_PLUS = "RASPBERRY_PI_3B_PLUS"
RASPBERRY_PI_CM3 = "RASPBERRY_PI_CM3"
RASPBERRY_PI_3A_PLUS = "RASPBERRY_PI_3A_PLUS"

# TODO: Should this include RASPBERRY_PI_3A_PLUS or any other models?
ANY_RASPBERRY_PI_2_OR_3 = (
    RASPBERRY_PI_2B,
    RASPBERRY_PI_3B,
    RASPBERRY_PI_3B_PLUS
)

_PI_REV_CODES = {
    RASPBERRY_PI_B: ('0002', '0003', '0004', '0005', '0006', '000d', '000e', '000f'),
    RASPBERRY_PI_B_PLUS: ('0010', '0013', '900032'),
    RASPBERRY_PI_A: ('0007', '0008', '0009'),
    RASPBERRY_PI_A_PLUS: ('0012', '0015', '900021'),
    RASPBERRY_PI_CM1: ('0011', '0014'),
    RASPBERRY_PI_ZERO: ('900092', '920092', '900093', '920093'),
    RASPBERRY_PI_ZERO_W: ('9000c1',),
    RASPBERRY_PI_2B: ('a01040', 'a01041', 'a21041', 'a22042'),
    RASPBERRY_PI_3B: ('a22082', 'a32082', 'a52082'),
    RASPBERRY_PI_3B_PLUS: ('a020d3',),
    RASPBERRY_PI_CM3: ('a020a0',),
    RASPBERRY_PI_3A_PLUS: ('9020e0',),
}

class Board:
    """
    Attempt to detect specific boards.
    """
    def __init__(self, detect):
        self.detect = detect

    @property
    def id(self):
        """Return a unique id for the detected board, if any."""

        chip_id = self.detect.chip.id

        if chip_id == ap_chip.BCM2XXX:
            return self._pi_id()
        elif chip_id == ap_chip.AM33XX:
            return BEAGLEBONE_BLACK
        elif chip_id == ap_chip.SUN8I:
            return self._armbian_id()
        elif chip_id == ap_chip.ESP8266:
            return FEATHER_HUZZAH
        elif chip_id == ap_chip.SAMD21:
            return FEATHER_M0_EXPRESS
        elif chip_id == ap_chip.STM32:
            return PYBOARD

        return None

    def _pi_id(self):
        """Try to detect id of a Raspberry Pi."""
        # Check for Pi boards:
        pi_rev_code = self._pi_rev_code()
        if pi_rev_code:
            for model, codes in _PI_REV_CODES.items():
                if pi_rev_code in codes:
                    return model
        return None

    def _pi_rev_code(self):
        """Attempt to find a Raspberry Pi revision code for this board."""
        # 2708 is Pi 1
        # 2709 is Pi 2
        # 2835 is Pi 3 (or greater) on 4.9.x kernel
        # Anything else is not a Pi.
        if self.detect.chip.id != ap_chip.BCM2XXX:
            # Something else, not a Pi.
            return None
        return self.detect.get_cpuinfo_field('Revision')

    @property
    def _armbian_id(self):
        """Check whether the current board is an OrangePi PC."""
        board_value = self.detect.get_armbian_release_field('BOARD')
        if board_value == "orangepipc":
            return ORANGE_PI_PC
        return None

    @property
    def beaglebone_black(self):
        """Check whether the current board is a Beaglebone Black."""
        return self.id == BEAGLEBONE_BLACK

    @property
    def orange_pi_pc(self):
        """Check whether the current board is an Orange Pi PC."""
        return self.id == ORANGE_PI_PC

    @property
    def any_raspberry_pi(self):
        """Check whether the current board is any Raspberry Pi."""
        return self._pi_rev_code() is not None

    @property
    def any_raspberry_pi_2_or_3(self):
        return self.id in ANY_RASPBERRY_PI_2_OR_3

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected board.  See list
        of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        else:
            return False

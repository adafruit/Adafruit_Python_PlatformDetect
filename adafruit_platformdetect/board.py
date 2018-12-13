"""Detect boards."""
import adafruit_platformdetect.chip as ap_chip

# Allow for aligned constant definitions:
# pylint: disable=bad-whitespace
BEAGLEBONE                  = 'BEAGLEBONE'
BEAGLEBONE_BLACK            = 'BEAGLEBONE_BLACK'
BEAGLEBONE_BLUE             = 'BEAGLEBONE_BLUE'
BEAGLEBONE_BLACK_WIRELESS   = 'BEAGLEBONE_BLACK_WIRELESS'
BEAGLEBONE_POCKETBEAGLE     = 'BEAGLEBONE_POCKETBEAGLE'
BEAGLEBONE_GREEN            = 'BEAGLEBONE_GREEN'
BEAGLEBONE_GREEN_WIRELESS   = 'BEAGLEBONE_GREEN_WIRELESS'
BEAGLEBONE_BLACK_INDUSTRIAL = 'BEAGLEBONE_BLACK_INDUSTRIAL'
BEAGLEBONE_ENHANCED         = 'BEAGLEBONE_ENHANCED'
BEAGLEBONE_USOMIQ           = 'BEAGLEBONE_USOMIQ'
BEAGLEBONE_AIR              = 'BEAGLEBONE_AIR'
BEAGLEBONE_POCKETBONE       = 'BEAGLEBONE_POCKETBONE'
BEAGLELOGIC_STANDALONE      = 'BEAGLELOGIC_STANDALONE'
OSD3358_DEV_BOARD           = 'OSD3358_DEV_BOARD'
OSD3358_SM_RED              = 'OSD3358_SM_RED'

FEATHER_HUZZAH              = "FEATHER_HUZZAH"
FEATHER_M0_EXPRESS          = "FEATHER_M0_EXPRESS"
GENERIC_LINUX_PC            = "GENERIC_LINUX_PC"
PYBOARD                     = "PYBOARD"
NODEMCU                     = "NODEMCU"
ORANGE_PI_PC                = "ORANGE_PI_PC"

RASPBERRY_PI_B              = "RASPBERRY_PI_B"
RASPBERRY_PI_B_PLUS         = "RASPBERRY_PI_B_PLUS"
RASPBERRY_PI_A              = "RASPBERRY_PI_A"
RASPBERRY_PI_A_PLUS         = "RASPBERRY_PI_A_PLUS"
RASPBERRY_PI_CM1            = "RASPBERRY_PI_CM1"
RASPBERRY_PI_ZERO           = "RASPBERRY_PI_ZERO"
RASPBERRY_PI_ZERO_W         = "RASPBERRY_PI_ZERO_W"
RASPBERRY_PI_2B             = "RASPBERRY_PI_2B"
RASPBERRY_PI_3B             = "RASPBERRY_PI_3B"
RASPBERRY_PI_3B_PLUS        = "RASPBERRY_PI_3B_PLUS"
RASPBERRY_PI_CM3            = "RASPBERRY_PI_CM3"
RASPBERRY_PI_3A_PLUS        = "RASPBERRY_PI_3A_PLUS"
# pylint: enable=bad-whitespace

ANY_RASPBERRY_PI_2_OR_3 = (
    RASPBERRY_PI_2B,
    RASPBERRY_PI_3B,
    RASPBERRY_PI_3B_PLUS
)

# BeagleBone eeprom board ids from:
#   https://github.com/beagleboard/image-builder
# Thanks to zmatt on freenode #beagle for pointers.
_BEAGLEBONE_BOARD_IDS = {
    # Original bone/white:
    BEAGLEBONE: (
        ('A4', 'A335BONE00A4'),
        ('A5', 'A335BONE00A5'),
        ('A6', 'A335BONE00A6'),
        ('A6A', 'A335BONE0A6A'),
        ('A6B', 'A335BONE0A6B'),
        ('B', 'A335BONE000B'),
    ),
    BEAGLEBONE_BLACK: (
        ('A5', 'A335BNLT00A5'),
        ('A5A', 'A335BNLT0A5A'),
        ('A5B', 'A335BNLT0A5B'),
        ('A5C', 'A335BNLT0A5C'),
        ('A6', 'A335BNLT00A6'),
        ('C', 'A335BNLT000C'),
        ('C', 'A335BNLT00C0'),
    ),
    BEAGLEBONE_BLUE: (
        ('A2', 'A335BNLTBLA2'),
    ),
    BEAGLEBONE_BLACK_WIRELESS: (
        ('A5', 'A335BNLTBWA5'),
    ),
    BEAGLEBONE_POCKETBEAGLE: (
        ('A2', 'A335PBGL00A2'),
    ),
    BEAGLEBONE_GREEN: (
        ('1A', 'A335BNLT....'),
        ('UNKNOWN', 'A335BNLTBBG1'),
    ),
    BEAGLEBONE_GREEN_WIRELESS: (
        ('W1A', 'A335BNLTGW1A'),
    ),
    BEAGLEBONE_BLACK_INDUSTRIAL: (
        ('A0', 'A335BNLTAIA0'), # Arrow
        ('A0', 'A335BNLTEIA0'), # Element14
    ),
    BEAGLEBONE_ENHANCED: (
        ('A', 'A335BNLTSE0A'),
    ),
    BEAGLEBONE_USOMIQ: (
        ('6', 'A335BNLTME06'),
    ),
    BEAGLEBONE_AIR: (
        ('A0', 'A335BNLTNAD0'),
    ),
    BEAGLEBONE_POCKETBONE: (
        ('0', 'A335BNLTBP00'),
    ),
    OSD3358_DEV_BOARD: (
        ('0.1', 'A335BNLTGH01'),
    ),
    OSD3358_SM_RED: (
        ('0', 'A335BNLTOS00'),
    ),
    BEAGLELOGIC_STANDALONE: (
        ('A', 'A335BLGC000A'),
    )
}

# Pi revision codes from:
#   https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md

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
    """Attempt to detect specific boards."""
    def __init__(self, detector):
        self.detector = detector

    # pylint: disable=invalid-name
    @property
    def id(self):
        """Return a unique id for the detected board, if any."""

        chip_id = self.detector.chip.id
        board_id = None

        if chip_id == ap_chip.BCM2XXX:
            board_id = self._pi_id()
        elif chip_id == ap_chip.AM33XX:
            board_id = self._beaglebone_id()
        elif chip_id == ap_chip.GENERIC_X86:
            board_id = GENERIC_LINUX_PC
        elif chip_id == ap_chip.SUN8I:
            board_id = self._armbian_id()
        elif chip_id == ap_chip.ESP8266:
            board_id = FEATHER_HUZZAH
        elif chip_id == ap_chip.SAMD21:
            board_id = FEATHER_M0_EXPRESS
        elif chip_id == ap_chip.STM32:
            board_id = PYBOARD

        return board_id
    # pylint: enable=invalid-name

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
        if self.detector.chip.id != ap_chip.BCM2XXX:
            # Something else, not a Pi.
            return None
        return self.detector.get_cpuinfo_field('Revision')

    # pylint: disable=no-self-use
    def _beaglebone_id(self):
        """Try to detect id of a Beaglebone."""
        try:
            with open("/sys/bus/nvmem/devices/0-00500/nvmem", "rb") as eeprom:
                eeprom_bytes = eeprom.read(16)
        except FileNotFoundError:
            return None

        if eeprom_bytes[:4] != b'\xaaU3\xee':
            return None

        id_string = eeprom_bytes[4:].decode("ascii")
        for model, bb_ids in _BEAGLEBONE_BOARD_IDS.items():
            for bb_id in bb_ids:
                if id_string == bb_id[1]:
                    return model

        return None
    # pylint: enable=no-self-use

    def _armbian_id(self):
        """Check whether the current board is an OrangePi PC."""
        board_value = self.detector.get_armbian_release_field('BOARD')
        if board_value == "orangepipc":
            return ORANGE_PI_PC
        return None

    @property
    def any_raspberry_pi(self):
        """Check whether the current board is any Raspberry Pi."""
        return self._pi_rev_code() is not None

    @property
    def any_raspberry_pi_2_or_3(self):
        """Check whether the current board is any Raspberry Pi 2 or 3."""
        return self.id in ANY_RASPBERRY_PI_2_OR_3

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected board.  See list
        of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

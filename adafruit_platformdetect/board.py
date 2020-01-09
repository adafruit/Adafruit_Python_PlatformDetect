"""Detect boards."""
import os
import re

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
ORANGE_PI_R1                = "ORANGE_PI_R1"
ORANGE_PI_ZERO              = "ORANGE_PI_ZERO"
GIANT_BOARD                 = "GIANT_BOARD"

# NVIDIA Jetson boards
JETSON_TX1                  = 'JETSON_TX1'
JETSON_TX2                  = 'JETSON_TX2'
JETSON_XAVIER               = 'JETSON_XAVIER'
JETSON_NANO                 = 'JETSON_NANO'

# Google Coral dev board
CORAL_EDGE_TPU_DEV          = "CORAL_EDGE_TPU_DEV"

# Various Raspberry Pi models
RASPBERRY_PI_B_REV1         = "RASPBERRY_PI_B_REV1"
RASPBERRY_PI_B_REV2         = "RASPBERRY_PI_B_REV2"
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
RASPBERRY_PI_CM3_PLUS       = "RASPBERRY_PI_CM3_PLUS"
RASPBERRY_PI_4B             = "RASPBERRY_PI_4B"

ODROID_C1                   = "ODROID_C1"
ODROID_C1_PLUS              = "ODROID_C1_PLUS"
ODROID_C2                   = "ODROID_C2"
ODROID_N2                   = "ODROID_N2"

FTDI_FT232H                 = "FTDI_FT232H"
DRAGONBOARD_410C            = "DRAGONBOARD_410C"

SIFIVE_UNLEASHED            = "SIFIVE_UNLEASHED"

MICROCHIP_MCP2221           = "MICROCHIP_MCP2221"

BINHO_NOVA                  = "BINHO_NOVA"

ONION_OMEGA                 = "ONION_OMEGA"
ONION_OMEGA2                = "ONION_OMEGA2"

PINE64 = "PINE64"
PINEBOOK = "PINEBOOK"
PINEPHONE = "PINEPHONE"

# pylint: enable=bad-whitespace

#OrangePI
_ORANGE_PI_IDS = (
    ORANGE_PI_PC,
    ORANGE_PI_R1,
    ORANGE_PI_ZERO
)

_CORAL_IDS = (
    CORAL_EDGE_TPU_DEV,
)

_JETSON_IDS = (
    JETSON_TX1,
    JETSON_TX2,
    JETSON_XAVIER,
    JETSON_NANO
)

_RASPBERRY_PI_40_PIN_IDS = (
    RASPBERRY_PI_B_PLUS,
    RASPBERRY_PI_A_PLUS,
    RASPBERRY_PI_ZERO,
    RASPBERRY_PI_ZERO_W,
    RASPBERRY_PI_2B,
    RASPBERRY_PI_3B,
    RASPBERRY_PI_3B_PLUS,
    RASPBERRY_PI_3A_PLUS,
    RASPBERRY_PI_4B
)

_RASPBERRY_PI_CM_IDS = (
    RASPBERRY_PI_CM1,
    RASPBERRY_PI_CM3,
    RASPBERRY_PI_CM3_PLUS
)

_ODROID_40_PIN_IDS = (
    ODROID_C1,
    ODROID_C1_PLUS,
    ODROID_C2,
    ODROID_N2
)

_BEAGLEBONE_IDS = (
    BEAGLEBONE,
    BEAGLEBONE_BLACK,
    BEAGLEBONE_BLUE,
    BEAGLEBONE_BLACK_WIRELESS,
    BEAGLEBONE_POCKETBEAGLE,
    BEAGLEBONE_GREEN,
    BEAGLEBONE_GREEN_WIRELESS,
    BEAGLEBONE_BLACK_INDUSTRIAL,
    BEAGLEBONE_ENHANCED,
    BEAGLEBONE_USOMIQ,
    BEAGLEBONE_AIR,
    BEAGLEBONE_POCKETBONE,
    BEAGLELOGIC_STANDALONE,
    OSD3358_DEV_BOARD,
    OSD3358_SM_RED,
)

_LINARO_96BOARDS_IDS = (
    DRAGONBOARD_410C,
)


_SIFIVE_IDS = (
    SIFIVE_UNLEASHED,
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

# Each tuple here contains both the base codes, and the versions that indicate
# the Pi is overvolted / overclocked - for 4-digit codes, this will be prefixed
# with 1000, and for 6-digit codes it'll be prefixed with 1.  These are placed
# on separate lines.

_PI_REV_CODES = {
    RASPBERRY_PI_B_REV1: (
        # Regular codes:
        '0002', '0003',

        # Overvolted/clocked versions:
        '1000002', '1000003',
    ),
    RASPBERRY_PI_B_REV2: (
        '0005', '0006', '000d', '000e', '000f',
        '1000005', '1000006', '100000d', '100000e', '100000f',
    ),
    RASPBERRY_PI_B_PLUS: (
        '0010', '0013', '900032',
        '1000010', '1000013', '1900032',
    ),
    RASPBERRY_PI_A: (
        '0007', '0008', '0009',
        '1000007', '1000008', '1000009',
    ),
    RASPBERRY_PI_A_PLUS: (
        '0012', '0015', '900021',
        '1000012', '1000015', '1900021',
    ),
    RASPBERRY_PI_CM1: (
        '0011', '0014',
        '10000011', '10000014',
    ),
    RASPBERRY_PI_ZERO: (
        '900092', '920092', '900093', '920093',
        '1900092', '1920092', '1900093', '1920093',  # warranty bit 24
        '2900092', '2920092', '2900093', '2920093',  # warranty bit 25
    ),
    RASPBERRY_PI_ZERO_W: (
        '9000c1',
        '19000c1', '29000c1',  # warranty bits
    ),
    RASPBERRY_PI_2B: (
        'a01040', 'a01041', 'a21041', 'a22042',
        '1a01040', '1a01041', '1a21041', '1a22042',  # warranty bit 24
        '2a01040', '2a01041', '2a21041', '2a22042',  # warranty bit 25
    ),
    RASPBERRY_PI_3B: (
        'a02082', 'a22082', 'a32082', 'a52082',
        '1a02082', '1a22082', '1a32082', '1a52082',  # warranty bit 24
        '2a02082', '2a22082', '2a32082', '2a52082',  # warranty bit 25
    ),
    RASPBERRY_PI_3B_PLUS: (
        'a020d3',
        '1a020d3', '2a020d3',  # warranty bits
    ),
    RASPBERRY_PI_CM3: (
        'a020a0', 'a220a0',
        '1a020a0', '2a020a0',  # warranty bits
        '1a220a0', '2a220a0',
    ),
    RASPBERRY_PI_3A_PLUS: (
        '9020e0',
        '19020e0', '29020e0',  # warranty bits
    ),
    RASPBERRY_PI_CM3_PLUS: (
        'a02100',
        '1a02100', '2a02100',  # warranty bits
    ),
    RASPBERRY_PI_4B: (
        'a03111', 'b03111', 'c03111',
        'a03112', 'b03112', 'c03112',
        '1a03111', '2a03111', '1b03111', '2b03111',  # warranty bits
        '1c03111', '2c03111', '1a03112', '2a03112',
        '1b03112', '2b03112', '1c03112', '2c03112',
    ),
}

# Onion omega boards
_ONION_OMEGA_BOARD_IDS = (
    ONION_OMEGA,
    ONION_OMEGA2,
)

# Pine64 boards and devices
_PINE64_DEV_IDS = (
    PINE64,
    PINEBOOK,
    PINEPHONE
)

class Board:
    """Attempt to detect specific boards."""
    def __init__(self, detector):
        self.detector = detector

    # pylint: disable=invalid-name, too-many-branches
    @property
    def id(self):
        """Return a unique id for the detected board, if any."""
        # There are some times we want to trick the platform detection
        # say if a raspberry pi doesn't have the right ID, or for testing
        try:
            return os.environ['BLINKA_FORCEBOARD']
        except KeyError: # no forced board, continue with testing!
            pass

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
        elif chip_id == ap_chip.SAMA5:
            board_id = self._sama5_id()
        elif chip_id == ap_chip.IMX8MX:
            board_id = self._imx8mx_id()
        elif chip_id == ap_chip.ESP8266:
            board_id = FEATHER_HUZZAH
        elif chip_id == ap_chip.SAMD21:
            board_id = FEATHER_M0_EXPRESS
        elif chip_id == ap_chip.STM32:
            board_id = PYBOARD
        elif chip_id == ap_chip.S805:
            board_id = ODROID_C1
        elif chip_id == ap_chip.S905:
            board_id = ODROID_C2
        elif chip_id == ap_chip.S922X:
            board_id = ODROID_N2
        elif chip_id == ap_chip.FT232H:
            board_id = FTDI_FT232H
        elif chip_id == ap_chip.APQ8016:
            board_id = DRAGONBOARD_410C
        elif chip_id in (ap_chip.T210, ap_chip.T186, ap_chip.T194):
            board_id = self._tegra_id()
        elif chip_id == ap_chip.HFU540:
            board_id = self._sifive_id()
        elif chip_id == ap_chip.MCP2221:
            board_id = MICROCHIP_MCP2221
        elif chip_id == ap_chip.BINHO:
            board_id = BINHO_NOVA
        elif chip_id == ap_chip.MIPS24KC:
            board_id = ONION_OMEGA
        elif chip_id == ap_chip.MIPS24KEC:
            board_id = ONION_OMEGA2
        elif chip_id == ap_chip.A64:
            board_id = self._pine64_id()
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

        # We may be on a non-Raspbian OS, so try to lazily determine
        # the version based on `get_device_model`
        else:
            pi_model = self.detector.get_device_model()
            if pi_model:
                pi_model = pi_model.upper().replace(' ', '_')
                if "PLUS" in pi_model:
                    re_model = re.search(r'(RASPBERRY_PI_\d).*([AB]_*)(PLUS)',
                                         pi_model)
                elif "CM" in pi_model: # untested for Compute Module
                    re_model = re.search(r'(RASPBERRY_PI_CM)(\d)',
                                         pi_model)
                else: # untested for non-plus models
                    re_model = re.search(r'(RASPBERRY_PI_\d).*([AB]_*)',
                                         pi_model)

                if re_model:
                    pi_model = "".join(re_model.groups())
                    available_models = _PI_REV_CODES.keys()
                    for model in available_models:
                        if model == pi_model:
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
        """Check whether the current board is an OrangePi PC or OrangePI R1."""
        board_value = self.detector.get_armbian_release_field('BOARD')
        if board_value == "orangepipc":
            return ORANGE_PI_PC
        if board_value == "orangepi-r1":
            return ORANGE_PI_R1
        if board_value == "orangepizero":
            return ORANGE_PI_ZERO
        if board_value == "pinebook-a64":
            return PINEBOOK
        return None

    def _sama5_id(self):
        """Check what type sama5 board."""
        board_value = self.detector.get_device_model()
        if "Giant Board" in board_value:
            return GIANT_BOARD
        return None

    def _imx8mx_id(self):
        """Check what type iMX8M board."""
        board_value = self.detector.get_device_model()
        if "Phanbell" in board_value:
            return CORAL_EDGE_TPU_DEV
        return None

    def _tegra_id(self):
        """Try to detect the id of aarch64 board."""
        board_value = self.detector.get_device_model()
        board = None
        if 'tx1' in board_value.lower():
            board = JETSON_TX1
        elif 'quill' in board_value or "storm" in board_value or "lightning" in board_value:
            board = JETSON_TX2
        elif 'xavier' in board_value.lower() or 'agx' in board_value.lower():
            board = JETSON_XAVIER
        elif 'nano' in board_value.lower():
            board = JETSON_NANO
        return board

    def _sifive_id(self):
        """Try to detect the id for Sifive RISCV64 board."""
        board_value = self.detector.get_device_model()
        if 'hifive-unleashed-a00' in board_value:
            return SIFIVE_UNLEASHED
        return None

    def _pine64_id(self):
        """Try to detect the id for Pine64 board or device."""
        board_value = self.detector.get_device_model()
        board = None
        if 'pine64' in board_value.lower():
            board = PINE64
        elif 'pinebook' in board_value.lower():
            board = PINEBOOK
        elif 'pinephone' in board_value.lower():
            board = PINEPHONE
        return board

    @property
    def any_96boards(self):
        """Check whether the current board is any 96boards board."""
        return self.id in _LINARO_96BOARDS_IDS

    @property
    def any_raspberry_pi(self):
        """Check whether the current board is any Raspberry Pi."""
        return self._pi_rev_code() is not None

    @property
    def any_raspberry_pi_40_pin(self):
        """Check whether the current board is any 40-pin Raspberry Pi."""
        return self.id in _RASPBERRY_PI_40_PIN_IDS

    @property
    def any_raspberry_pi_cm(self):
        """Check whether the current board is any Compute Module Raspberry Pi."""
        return self.id in _RASPBERRY_PI_CM_IDS

    @property
    def any_beaglebone(self):
        """Check whether the current board is any Beaglebone-family system."""
        return self.id in _BEAGLEBONE_IDS

    @property
    def any_orange_pi(self):
        """Check whether the current board is any defined Orange Pi."""
        return self.id in _ORANGE_PI_IDS

    @property
    def any_coral_board(self):
        """Check whether the current board is any defined Coral."""
        return self.CORAL_EDGE_TPU_DEV

    @property
    def any_giant_board(self):
        """Check whether the current board is any defined Giant Board."""
        return self.GIANT_BOARD

    @property
    def any_odroid_40_pin(self):
        """Check whether the current board is any defined 40-pin Odroid."""
        return self.id in _ODROID_40_PIN_IDS

    @property
    def any_jetson_board(self):
        """Check whether the current board is any defined Jetson Board."""
        return self.id in _JETSON_IDS

    @property
    def any_sifive_board(self):
        """Check whether the current board is any defined Jetson Board."""
        return self.id in _SIFIVE_IDS

    @property
    def any_onion_omega_board(self):
        """Check whether the current board is any defined OpenWRT board."""
        return self.id in _ONION_OMEGA_BOARD_IDS

    @property
    def any_pine64_board(self):
        """Check whether the current board is any Pine64 device."""
        return self.id in _PINE64_DEV_IDS

    @property
    def any_embedded_linux(self):
        """Check whether the current board is any embedded Linux device."""
        return self.any_raspberry_pi or self.any_beaglebone or \
         self.any_orange_pi or self.any_giant_board or self.any_jetson_board or \
         self.any_coral_board or self.any_odroid_40_pin or self.any_96boards or \
         self.any_sifive_board or self.any_onion_omega_board or self.any_pine64_board

    @property
    def ftdi_ft232h(self):
        """Check whether the current board is an FTDI FT232H."""
        return self.id == FTDI_FT232H

    @property
    def microchip_mcp2221(self):
        """Check whether the current board is a Microchip MCP2221."""
        return self.id == MICROCHIP_MCP2221

    @property
    def binho_nova(self):
        """Check whether the current board is an BINHO NOVA."""
        return self.id == BINHO_NOVA

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected board.  See list
        of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

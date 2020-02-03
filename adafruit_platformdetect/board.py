"""Detect boards."""
import os
import re

# Allow for aligned constant definitions:
# pylint: disable=bad-whitespace
from adafruit_platformdetect.constants import boards, chips


class Board:
    """Attempt to detect specific boards."""

    def __init__(self, detector):
        self.detector = detector

    # pylint: disable=invalid-name, protected-access
    @property
    def id(self):
        """Return a unique id for the detected board, if any."""
        # There are some times we want to trick the platform detection
        # say if a raspberry pi doesn't have the right ID, or for testing
        try:
            return os.environ['BLINKA_FORCEBOARD']

        except KeyError:  # no forced board, continue with testing!
            pass

        chip_id = self.detector.chip.id
        # Relationship chip-board.
        boards_chip = {
            chips.A64:          self._pine64_id,
            chips.AM33XX:       self._beaglebone_id,
            chips.APQ8016:      boards.DRAGONBOARD_410C,
            chips.BCM2XXX:      self._pi_id,
            chips.BINHO:        boards.BINHO_NOVA,
            chips.ESP8266:      boards.FEATHER_HUZZAH,
            chips.FT232H:       boards.FTDI_FT232H,
            chips.GENERIC_X86:  boards.GENERIC_LINUX_PC,
            chips.HFU540:       self._sifive_id,
            chips.IMX8MX:       self._imx8mx_id,
            chips.MCP2221:      boards.MICROCHIP_MCP2221,
            chips.MIPS24KC:     boards.ONION_OMEGA,
            chips.MIPS24KEC:    boards.ONION_OMEGA2,
            chips.S805:         boards.ODROID_C1,
            chips.S905:         boards.ODROID_C2,
            chips.S922X:        boards.ODROID_N2,
            chips.SAMA5:        self._sama5_id,
            chips.SAMD21:       boards.FEATHER_M0_EXPRESS,
            chips.STM32:        boards.PYBOARD,
            chips.SUN8I:        self._armbian_id,
        }

        board_id = self.detector._get_value(boards_chip, chip_id)

        return board_id

    # pylint: enable=invalid-name

    def _pi_id(self):
        """Try to detect id of a Raspberry Pi."""
        # Check for Pi boards on Raspbian OS:
        pi_rev_code = self._pi_rev_code()

        if pi_rev_code:
            for model, codes in boards._PI_REV_CODES.items():
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
                elif "CM" in pi_model:  # untested for Compute Module
                    re_model = re.search(r'(RASPBERRY_PI_CM)(\d)',
                                         pi_model)
                else:  # untested for non-plus models
                    re_model = re.search(r'(RASPBERRY_PI_\d).*([AB])',
                                         pi_model)

                if re_model:
                    pi_model = "".join(re_model.groups())
                    available_models = boards._PI_REV_CODES.keys()

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
        if self.detector.chip.id != chips.BCM2XXX:
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

        # special condition for BeagleBone Green rev. 1A
        # refer to GitHub issue #57 in this repo for more info
        if eeprom_bytes == b'\xaaU3\xeeA335BNLT\x1a\x00\x00\x00':
            return boards.BEAGLEBONE_GREEN

        id_string = eeprom_bytes[4:].decode("ascii")
        for model, bb_ids in boards._BEAGLEBONE_BOARD_IDS.items():
            for bb_id in bb_ids:
                if id_string == bb_id[1]:
                    return model

        return None

    # pylint: enable=no-self-use

    # pylint: disable=protected-access
    def _armbian_id(self):
        """Check whether the current board is an OrangePi board."""
        board_value = self.detector.get_armbian_release_field('BOARD')
        armbian_board = {
            "orangepipc":       boards.ORANGE_PI_PC,
            "orangepi-r1":      boards.ORANGE_PI_R1,
            "orangepizero":     boards.ORANGE_PI_ZERO,
            "orangepione":      boards.ORANGE_PI_ONE,
            "orangepilite":     boards.ORANGE_PI_LITE,
            "orangepiplus2e":   boards.ORANGE_PI_PLUS_2E,
            "orangepipcplus":   boards.ORANGE_PI_PC_PLUS,
            "pinebook-a64":     boards.PINEBOOK,

        }

        board = self.detector._get_value(armbian_board, board_value)

        return board

    # pylint: enable=protected-access

    def _sama5_id(self):
        """Check what type sama5 board."""
        board_value = self.detector.get_device_model()

        if "Giant Board" in board_value:
            return boards.GIANT_BOARD

        return None

    def _imx8mx_id(self):
        """Check what type iMX8M board."""
        board_value = self.detector.get_device_model()

        if "Phanbell" in board_value:
            return boards.CORAL_EDGE_TPU_DEV

        return None

    def _tegra_id(self):
        """Try to detect the id of aarch64 board."""
        board_value = self.detector.get_device_model()
        board = None

        if 'tx1' in board_value.lower():
            board = boards.JETSON_TX1

        elif 'quill' in board_value or "storm" in board_value or "lightning" in board_value:
            board = boards.JETSON_TX2

        elif 'xavier' in board_value.lower() or 'agx' in board_value.lower():
            board = boards.JETSON_XAVIER

        elif 'nano' in board_value.lower():
            board = boards.JETSON_NANO
        return board

    def _sifive_id(self):
        """Try to detect the id for Sifive RISCV64 board."""
        board_value = self.detector.get_device_model()

        if 'hifive-unleashed-a00' in board_value:
            return boards.SIFIVE_UNLEASHED

        return None

    def _pine64_id(self):
        """Try to detect the id for Pine64 board or device."""
        board_value = self.detector.get_device_model()

        pine_boards = {
            'pine64': boards.PINE64,
            'pinebook': boards.PINEBOOK,
            'pinephone': boards.PINEPHONE
        }

        return self.detector._get_value(pine_boards, board_value.lower())

    @property
    def any_96boards(self):
        """Check whether the current board is any 96boards board."""
        return self.id in boards._LINARO_96BOARDS_IDS

    @property
    def any_raspberry_pi(self):
        """Check whether the current board is any Raspberry Pi."""
        return self._pi_rev_code() is not None

    @property
    def any_raspberry_pi_40_pin(self):
        """Check whether the current board is any 40-pin Raspberry Pi."""
        return self.id in boards._RASPBERRY_PI_40_PIN_IDS

    @property
    def any_raspberry_pi_cm(self):
        """Check whether the current board is any Compute Module Raspberry Pi."""
        return self.id in boards._RASPBERRY_PI_CM_IDS

    @property
    def any_beaglebone(self):
        """Check whether the current board is any Beaglebone-family system."""
        return self.id in boards._BEAGLEBONE_IDS

    @property
    def any_orange_pi(self):
        """Check whether the current board is any defined Orange Pi."""
        return self.id in boards._ORANGE_PI_IDS

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
        return self.id in boards._ODROID_40_PIN_IDS

    @property
    def any_jetson_board(self):
        """Check whether the current board is any defined Jetson Board."""
        return self.id in boards._JETSON_IDS

    @property
    def any_sifive_board(self):
        """Check whether the current board is any defined Jetson Board."""
        return self.id in boards._SIFIVE_IDS

    @property
    def any_onion_omega_board(self):
        """Check whether the current board is any defined OpenWRT board."""
        return self.id in boards._ONION_OMEGA_BOARD_IDS

    @property
    def any_pine64_board(self):
        """Check whether the current board is any Pine64 device."""
        return self.id in boards._PINE64_DEV_IDS

    @property
    def any_embedded_linux(self):
        """Check whether the current board is any embedded Linux device."""
        return any(
            [
                self.any_raspberry_pi, self.any_beaglebone, self.any_orange_pi,
                self.any_giant_board, self.any_jetson_board, self.any_coral_board,
                self.any_odroid_40_pin, self.any_96boards, self.any_sifive_board,
                self.any_onion_omega_board, self.any_pine64_board,
            ]
        )

    @property
    def ftdi_ft232h(self):
        """Check whether the current board is an FTDI FT232H."""
        return self.id == boards.FTDI_FT232H

    @property
    def microchip_mcp2221(self):
        """Check whether the current board is a Microchip MCP2221."""
        return self.id == boards.MICROCHIP_MCP2221

    @property
    def binho_nova(self):
        """Check whether the current board is an BINHO NOVA."""
        return self.id == boards.BINHO_NOVA

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected board.  See list
        of constants at the top of this module for available options.
        """

        if self.id == attr:
            return True

        return False

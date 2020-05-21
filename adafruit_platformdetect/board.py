# The MIT License (MIT)
#
# Copyright (c) 2020 Melissa LeBlanc-Williams for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_platformdetect.board`
================================================================================

Detect boards

* Author(s): Melissa LeBlanc-Williams

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.5 or Higher

"""

# imports
import os
import re
from adafruit_platformdetect.constants import boards, chips

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_PlatformDetect.git"


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
            return os.environ["BLINKA_FORCEBOARD"]
        except KeyError:  # no forced board, continue with testing!
            pass

        chip_id = self.detector.chip.id
        board_id = None

        if chip_id == chips.BCM2XXX:
            board_id = self._pi_id()
        elif chip_id == chips.AM33XX:
            board_id = self._beaglebone_id()
        elif chip_id == chips.GENERIC_X86:
            board_id = boards.GENERIC_LINUX_PC
        elif chip_id == chips.SUN8I:
            board_id = self._armbian_id()
        elif chip_id == chips.SAMA5:
            board_id = self._sama5_id()
        elif chip_id == chips.IMX8MX:
            board_id = self._imx8mx_id()
        elif chip_id == chips.ESP8266:
            board_id = boards.FEATHER_HUZZAH
        elif chip_id == chips.SAMD21:
            board_id = boards.FEATHER_M0_EXPRESS
        elif chip_id == chips.STM32:
            board_id = boards.PYBOARD
        elif chip_id == chips.S805:
            board_id = boards.ODROID_C1
        elif chip_id == chips.S905:
            board_id = boards.ODROID_C2
        elif chip_id == chips.S905X3:
            board_id = boards.ODROID_C4
        elif chip_id == chips.S922X:
            board_id = boards.ODROID_N2
        elif chip_id == chips.EXYNOS5422:
            board_id = boards.ODROID_XU4
        elif chip_id == chips.FT232H:
            board_id = boards.FTDI_FT232H
        elif chip_id == chips.APQ8016:
            board_id = boards.DRAGONBOARD_410C
        elif chip_id in (chips.T210, chips.T186, chips.T194):
            board_id = self._tegra_id()
        elif chip_id == chips.HFU540:
            board_id = self._sifive_id()
        elif chip_id == chips.MCP2221:
            board_id = boards.MICROCHIP_MCP2221
        elif chip_id == chips.BINHO:
            board_id = boards.BINHO_NOVA
        elif chip_id == chips.LPC4330:
            board_id = boards.GREATFET_ONE
        elif chip_id == chips.MIPS24KC:
            board_id = boards.ONION_OMEGA
        elif chip_id == chips.MIPS24KEC:
            board_id = boards.ONION_OMEGA2
        elif chip_id == chips.ZYNQ7000:
            board_id = self._pynq_id()
        elif chip_id == chips.A64:
            board_id = self._pine64_id()
        elif chip_id == chips.A33:
            board_id = self._clockwork_pi_id()
        elif chip_id == chips.RK3308:
            board_id = self._rock_pi_id()
        elif chip_id == chips.RYZEN_V1605B:
            board_id = self._udoo_id()

        return board_id

    # pylint: enable=invalid-name

    def _pi_id(self):
        """Try to detect id of a Raspberry Pi."""
        # Check for Pi boards:
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
                pi_model = pi_model.upper().replace(" ", "_")
                if "PLUS" in pi_model:
                    re_model = re.search(r"(RASPBERRY_PI_\d).*([AB]_*)(PLUS)", pi_model)
                elif "CM" in pi_model:  # untested for Compute Module
                    re_model = re.search(r"(RASPBERRY_PI_CM)(\d)", pi_model)
                else:  # untested for non-plus models
                    re_model = re.search(r"(RASPBERRY_PI_\d).*([AB])", pi_model)

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
        rev = self.detector.get_cpuinfo_field("Revision")

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

    # pylint: disable=no-self-use
    def _beaglebone_id(self):
        """Try to detect id of a Beaglebone."""
        try:
            with open("/sys/bus/nvmem/devices/0-00500/nvmem", "rb") as eeprom:
                eeprom_bytes = eeprom.read(16)
        except FileNotFoundError:
            return None

        if eeprom_bytes[:4] != b"\xaaU3\xee":
            return None

        # special condition for BeagleBone Green rev. 1A
        # refer to GitHub issue #57 in this repo for more info
        if eeprom_bytes == b"\xaaU3\xeeA335BNLT\x1a\x00\x00\x00":
            return boards.BEAGLEBONE_GREEN

        id_string = eeprom_bytes[4:].decode("ascii")
        for model, bb_ids in boards._BEAGLEBONE_BOARD_IDS.items():
            for bb_id in bb_ids:
                if id_string == bb_id[1]:
                    return model

        return None

    # pylint: enable=no-self-use

    # pylint: disable=too-many-return-statements
    def _armbian_id(self):
        """Check whether the current board is an OrangePi board."""
        board_value = self.detector.get_armbian_release_field("BOARD")
        board = None

        if board_value == "orangepipc":
            board = boards.ORANGE_PI_PC
        if board_value == "orangepi-r1":
            board = boards.ORANGE_PI_R1
        if board_value == "orangepizero":
            board = boards.ORANGE_PI_ZERO
        if board_value == "orangepione":
            board = boards.ORANGE_PI_ONE
        if board_value == "orangepilite":
            board = boards.ORANGE_PI_LITE
        if board_value == "orangepiplus2e":
            board = boards.ORANGE_PI_PLUS_2E
        if board_value == "orangepipcplus":
            board = boards.ORANGE_PI_PC_PLUS
        if board_value == "pinebook-a64":
            board = boards.PINEBOOK
        if board_value == "orangepi2":
            board = boards.ORANGE_PI_2

        return board

    # pylint: enable=too-many-return-statements

    # pylint: enable=too-many-return-statements

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
        compatible = self.detector.get_device_compatible()
        if not compatible:
            return None
        compats = compatible.split("\x00")
        for board_id, board_compats in boards._JETSON_IDS.items():
            if any(v in compats for v in board_compats):
                return board_id
        return None

    def _sifive_id(self):
        """Try to detect the id for Sifive RISCV64 board."""
        board_value = self.detector.get_device_model()
        if "hifive-unleashed-a00" in board_value:
            return boards.SIFIVE_UNLEASHED
        return None

    def _pine64_id(self):
        """Try to detect the id for Pine64 board or device."""
        board_value = self.detector.get_device_model()
        board = None
        if "pine64" in board_value.lower():
            board = boards.PINE64
        elif "pinebook" in board_value.lower():
            board = boards.PINEBOOK
        elif "pinephone" in board_value.lower():
            board = boards.PINEPHONE
        return board

    # pylint: disable=no-self-use
    def _pynq_id(self):
        """Try to detect the id for Xilinx PYNQ boards."""
        try:
            with open("/proc/device-tree/chosen/pynq_board", "r") as board_file:
                board_model = board_file.read()
                match = board_model.upper().replace("-", "_").rstrip("\x00")
                for model in boards._PYNQ_IDS:
                    if model == match:
                        return model

                return None

        except FileNotFoundError:
            return None

    def _rock_pi_id(self):
        """Check what type of Rock Pi board."""
        board_value = self.detector.get_device_model()
        board = None
        if board_value and "ROCK Pi S" in board_value:
            board = boards.ROCK_PI_S
        return board

    def _clockwork_pi_id(self):
        """Check what type of Clockwork Pi board."""
        board_value = self.detector.get_device_model()
        board = None
        if board_value and "Clockwork CPI3" in board_value:
            board = boards.CLOCKWORK_CPI3
        return board

    def _udoo_id(self):
        """Try to detect the id of udoo board."""
        board_asset_tag = self.detector.check_board_asset_tag_value()
        for board_id, board_tags in boards._UDOO_BOARD_IDS.items():
            if any(v == board_asset_tag for v in board_tags):
                return board_id
        return None

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
    def any_pynq_board(self):
        """Check whether the current board is any defined PYNQ Board."""
        return self.id in boards._PYNQ_IDS

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
    def any_rock_pi_board(self):
        """Check whether the current board is any Clockwork Pi device."""
        return self.ROCK_PI_S

    @property
    def any_clockwork_pi_board(self):
        """Check whether the current board is any Clockwork Pi device."""
        return self.CLOCKWORK_CPI3

    @property
    def any_udoo_board(self):
        """Check to see if the current board is an UDOO board"""
        return self.id in boards._UDOO_BOARD_IDS

    @property
    def any_embedded_linux(self):
        """Check whether the current board is any embedded Linux device."""
        return any(
            [
                self.any_raspberry_pi,
                self.any_beaglebone,
                self.any_orange_pi,
                self.any_giant_board,
                self.any_jetson_board,
                self.any_coral_board,
                self.any_odroid_40_pin,
                self.any_96boards,
                self.any_sifive_board,
                self.any_onion_omega_board,
                self.any_pine64_board,
                self.any_pynq_board,
                self.any_rock_pi_board,
                self.any_clockwork_pi_board,
                self.any_udoo_board,
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

    @property
    def greatfet_one(self):
        """Check whether the current board is a GreatFET One."""
        return self.id == boards.GREATFET_ONE

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected board.  See list
        of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

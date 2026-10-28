# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2222 USB detection without connected hardware."""

import os
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from adafruit_platformdetect import Detector
from adafruit_platformdetect.constants import boards, chips


class MCP2222Tests(unittest.TestCase):
    """Check the USB identity, board selection, and missing-device error."""

    def test_connected(self):
        finder = Mock(return_value=object())
        with patch.dict(os.environ, {"BLINKA_MCP2222": "1"}, clear=True):
            with patch.dict(
                sys.modules, {"libusb_package": SimpleNamespace(find=finder)}
            ):
                detector = Detector()
                self.assertEqual(detector.chip.id, chips.MCP2222)
                self.assertEqual(detector.board.id, boards.MICROCHIP_MCP2222)
                self.assertTrue(detector.board.microchip_mcp2222)
                self.assertTrue(detector.board.os_environ_board)
                self.assertFalse(detector.board.microchip_mcp2221)
                finder.assert_called_once_with(idVendor=0x04D8, idProduct=0x0B15)

    def test_missing(self):
        finder = Mock(return_value=None)
        with patch.dict(os.environ, {"BLINKA_MCP2222": "1"}, clear=True):
            with patch.dict(
                sys.modules, {"libusb_package": SimpleNamespace(find=finder)}
            ):
                with self.assertRaisesRegex(RuntimeError, "no MCP2222 device found"):
                    _ = Detector().chip.id

    def test_environment_board_family(self):
        for board_id in (
            boards.MICROCHIP_MCP2221,
            boards.FTDI_FT232H,
            boards.ITSYBITSY_U2IF,
        ):
            with self.subTest(board_id=board_id):
                with patch.dict(
                    os.environ, {"BLINKA_FORCEBOARD": board_id}, clear=True
                ):
                    self.assertTrue(Detector().board.os_environ_board)


if __name__ == "__main__":
    unittest.main()

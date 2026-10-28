# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Regression checks for environment-controlled board detection."""

import os
import unittest
from unittest.mock import patch

from adafruit_platformdetect import Detector
from adafruit_platformdetect.constants import boards


class EnvironmentBoardTests(unittest.TestCase):
    """Recognize bridge boards without classifying unrelated boards as bridges."""

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

    def test_unrelated_board(self):
        with patch.dict(
            os.environ, {"BLINKA_FORCEBOARD": "TEST_UNRELATED_BOARD"}, clear=True
        ):
            self.assertFalse(Detector().board.os_environ_board)


if __name__ == "__main__":
    unittest.main()

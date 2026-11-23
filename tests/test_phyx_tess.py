# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT

"""Allwinner T113 and Phyx Tess detection without hardware access."""

import os
import unittest
from unittest.mock import patch

from adafruit_platformdetect import Detector
from adafruit_platformdetect.constants import boards, chips

TESS_COMPATIBLE = "phyx,tess-t113\x00allwinner,sun8i-t113s\x00"
T113_COMPATIBLE = "vendor,other-t113-board\x00allwinner,sun8i-t113s\x00"


class PhyxTessTests(unittest.TestCase):
    """Detect the chip and board from /proc/device-tree/compatible."""

    def setUp(self):
        environment = patch.dict(os.environ, {}, clear=True)
        environment.start()
        self.addCleanup(environment.stop)
        for module in ("board", "chip"):
            platform = patch(f"adafruit_platformdetect.{module}.sys.platform", "linux")
            platform.start()
            self.addCleanup(platform.stop)

    @staticmethod
    def make_detector(compatible):
        detector = Detector()
        detector.get_device_compatible = lambda: compatible
        detector.get_device_model = lambda: "Phyx Tess T113-S3"
        detector.get_cpuinfo_field = lambda field: None
        detector.get_armbian_release_field = lambda field: None
        return detector

    def test_tess(self):
        detector = self.make_detector(TESS_COMPATIBLE)
        self.assertEqual(detector.chip.id, chips.T113)
        self.assertEqual(detector.board.id, boards.PHYX_TESS)
        self.assertTrue(detector.board.any_phyx_board)
        self.assertTrue(detector.board.any_embedded_linux)

    def test_other_t113_board(self):
        detector = self.make_detector(T113_COMPATIBLE)
        self.assertEqual(detector.chip.id, chips.T113)
        self.assertNotEqual(detector.board.id, boards.PHYX_TESS)
        self.assertFalse(detector.board.any_phyx_board)


if __name__ == "__main__":
    unittest.main()

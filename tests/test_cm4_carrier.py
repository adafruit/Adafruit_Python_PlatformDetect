# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CM4 carrier selection without reading host files or detecting hardware."""

import io
import os
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, mock_open, patch

from adafruit_platformdetect.board import Board
from adafruit_platformdetect.constants import boards, chips


class CM4CarrierTests(unittest.TestCase):
    """Exercise the real revision decoder and Board.id selection path."""

    def setUp(self):
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.opened = []
        self.contents = "RASPBERRY_PI_4B\n"
        self.file_error = None
        self.reader = patch("builtins.open", side_effect=self.open_file)
        self.reader.start()
        self.addCleanup(self.reader.stop)

    def open_file(self, filename, mode="r", encoding=None):
        # Unexpected filesystem access must fail instead of falling back to the
        # host's files. The revision fallback intentionally sees no DT revision.
        self.opened.append(filename)
        if filename == "/proc/device-tree/system/linux,revision":
            self.assertEqual(mode, "rb")
            raise FileNotFoundError(filename)
        self.assertEqual(filename, "/etc/cm4-board")
        self.assertEqual((mode, encoding), ("r", "utf-8"))
        if self.file_error is not None:
            raise self.file_error
        return io.StringIO(self.contents)

    @staticmethod
    def make_board(revision="a03140", chip_id=chips.BCM2XXX, model=None):
        detector = SimpleNamespace(
            chip=SimpleNamespace(id=chip_id),
            get_cpuinfo_field=Mock(return_value=revision),
            get_device_model=Mock(return_value=model),
        )
        return Board(detector)

    def test_cm4_and_cm4s_override(self):
        for revision in ("a03140", "a03150"):
            for contents in ("RASPBERRY_PI_4B", " \tRASPBERRY_PI_4B\r\n"):
                with self.subTest(revision=revision, contents=contents):
                    self.contents = contents
                    self.assertEqual(
                        self.make_board(revision).id, boards.RASPBERRY_PI_4B
                    )

    def test_registered_carrier(self):
        # New carriers still require registration and Blinka routing; no actual
        # carrier support is invented by this selection mechanism.
        self.contents = "EXAMPLE_CM4_CARRIER\n"
        with patch.object(boards, "EXAMPLE_CM4_CARRIER", "CARRIER_ID", create=True):
            self.assertEqual(self.make_board().id, "CARRIER_ID")

    def test_constant_value(self):
        self.contents = "RASPBERRY_PI_AVNET_IIOT_GW"
        self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_AVNET_IIOT_GW)

    def test_invalid_contents_fall_back(self):
        for contents in (
            "",
            " \t\r\n",
            "UNKNOWN_CM4_CARRIER",
            "raspberry_pi_4b",
            "RASPBERRY_PI_4B\nRASPBERRY_PI_CM4",
            "board=RASPBERRY_PI_4B",
            "adafruit_blinka.board.raspberrypi.raspi_4b",
            "__doc__",
            "__name__",
            "_RASPBERRY_PI_4_IDS",
            "_PI_MODELS",
        ):
            with self.subTest(contents=contents):
                self.contents = contents
                self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_CM4)

    def test_file_failures_fall_back(self):
        for error in (
            FileNotFoundError(),
            PermissionError(),
            IsADirectoryError(),
            OSError("read failed"),
            UnicodeDecodeError("utf-8", b"\xff", 0, 1, "invalid UTF-8"),
        ):
            with self.subTest(error=error):
                self.file_error = error
                self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_CM4)

    def test_read_failure_falls_back(self):
        reader = mock_open()
        reader.return_value.read.side_effect = OSError("read failed")
        with patch("builtins.open", reader):
            self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_CM4)

    def test_model_fallback(self):
        board = self.make_board(revision=None, model="Raspberry Pi CM4")
        self.assertEqual(board.id, boards.RASPBERRY_PI_4B)
        self.assertEqual(
            self.opened,
            ["/proc/device-tree/system/linux,revision", "/etc/cm4-board"],
        )

    def test_other_pi_models(self):
        for revision, expected in (
            ("000e", boards.RASPBERRY_PI_B_REV2),
            ("a02082", boards.RASPBERRY_PI_3B),
            ("a020a0", boards.RASPBERRY_PI_CM3),
            ("a03111", boards.RASPBERRY_PI_4B),
            ("d04170", boards.RASPBERRY_PI_5),
            ("a04180", boards.RASPBERRY_PI_CM5),
        ):
            with self.subTest(revision=revision):
                self.assertEqual(self.make_board(revision).id, expected)
        self.assertEqual(self.opened, [])

    def test_unidentified_pi(self):
        self.assertIsNone(self.make_board(revision=None).id)
        self.assertEqual(self.opened, ["/proc/device-tree/system/linux,revision"])

    def test_other_platform(self):
        board = self.make_board(chip_id=chips.OS_AGNOSTIC)
        self.assertEqual(board.id, boards.OS_AGNOSTIC_BOARD)
        board.detector.get_cpuinfo_field.assert_not_called()
        self.assertEqual(self.opened, [])

    def test_environment_precedence(self):
        with patch.dict(os.environ, {"BLINKA_FORCEBOARD": "EXPLICIT_BOARD"}):
            board = self.make_board()
            self.assertEqual(board.id, "EXPLICIT_BOARD")
            board.detector.get_cpuinfo_field.assert_not_called()
        self.assertEqual(self.opened, [])

    def test_missing_environ(self):
        with patch("adafruit_platformdetect.board.os", SimpleNamespace()):
            self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_4B)

    def test_override_cached(self):
        board = self.make_board()
        self.assertEqual(board.id, boards.RASPBERRY_PI_4B)
        self.contents = "RASPBERRY_PI_CM4"
        self.assertEqual(board.id, boards.RASPBERRY_PI_4B)
        self.assertEqual(self.opened, ["/etc/cm4-board"])

    def test_fallback_cached(self):
        self.contents = "UNKNOWN"
        board = self.make_board()
        self.assertEqual(board.id, boards.RASPBERRY_PI_CM4)
        self.contents = "RASPBERRY_PI_4B"
        self.assertEqual(board.id, boards.RASPBERRY_PI_CM4)
        self.assertEqual(self.opened, ["/etc/cm4-board"])

    def test_new_detector(self):
        self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_4B)
        self.contents = "RASPBERRY_PI_CM4"
        self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_CM4)

    def test_chip_and_families(self):
        board = self.make_board()
        self.assertEqual(board.id, boards.RASPBERRY_PI_4B)
        self.assertEqual(board.detector.chip.id, chips.BCM2XXX)
        self.assertTrue(board.any_raspberry_pi)
        self.assertTrue(board.any_raspberry_pi_4_board)
        self.assertTrue(board.any_raspberry_pi_40_pin)
        self.assertFalse(board.any_raspberry_pi_5_board)


if __name__ == "__main__":
    unittest.main()

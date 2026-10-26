# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Explicit board selection without host-file or hardware access."""

import io
import os
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, mock_open, patch

from adafruit_platformdetect.board import Board
from adafruit_platformdetect.constants import boards, chips


COMPUTE_MODULE_REVISIONS = (
    ("0011", boards.RASPBERRY_PI_CM1),
    ("a020a0", boards.RASPBERRY_PI_CM3),
    ("a02100", boards.RASPBERRY_PI_CM3_PLUS),
    ("a03140", boards.RASPBERRY_PI_CM4),
    ("a03150", boards.RASPBERRY_PI_CM4S),
    ("a04180", boards.RASPBERRY_PI_CM5),
    ("a041a0", boards.RASPBERRY_PI_CM5_LITE),
)


class BoardOverrideTests(unittest.TestCase):
    """Exercise the real revision decoder and Board.id selection path."""

    def setUp(self):
        self.environment = patch.dict(os.environ, {}, clear=True)
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.platform = patch("adafruit_platformdetect.board.sys.platform", "linux")
        self.platform.start()
        self.addCleanup(self.platform.stop)
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
        self.assertEqual(filename, "/etc/blinka-board")
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

    def test_all_cm_overrides(self):
        for revision, _ in COMPUTE_MODULE_REVISIONS:
            for contents in ("RASPBERRY_PI_4B", " \tRASPBERRY_PI_4B\r\n"):
                with self.subTest(revision=revision, contents=contents):
                    self.contents = contents
                    self.assertEqual(
                        self.make_board(revision).id, boards.RASPBERRY_PI_4B
                    )

    def test_all_cm_fixtures(self):
        # Cover every currently supported Raspberry Pi Compute Module.
        self.assertCountEqual(
            [board_id for _, board_id in COMPUTE_MODULE_REVISIONS],
            boards._RASPBERRY_PI_CM_IDS,  # pylint: disable=protected-access
        )

    def test_each_module_fallback(self):
        for revision, expected in COMPUTE_MODULE_REVISIONS:
            for error in (None, FileNotFoundError(), PermissionError()):
                with self.subTest(revision=revision, error=error):
                    self.contents = "UNKNOWN_CM_CARRIER"
                    self.file_error = error
                    self.assertEqual(self.make_board(revision).id, expected)

    def test_registered_carrier(self):
        # New carriers still require registration and Blinka routing; no actual
        # carrier support is invented by this selection mechanism.
        self.contents = "EXAMPLE_CM_CARRIER\n"
        with patch.object(boards, "EXAMPLE_CM_CARRIER", "CARRIER_ID", create=True):
            for revision, _ in COMPUTE_MODULE_REVISIONS:
                with self.subTest(revision=revision):
                    self.assertEqual(self.make_board(revision).id, "CARRIER_ID")

    def test_constant_value(self):
        self.contents = "RASPBERRY_PI_AVNET_IIOT_GW"
        self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_AVNET_IIOT_GW)

    def test_invalid_contents_fall_back(self):
        for contents in (
            "",
            " \t\r\n",
            "UNKNOWN_CM_CARRIER",
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
        self.contents = "UNKNOWN"
        for model, expected in (
            ("CM1", boards.RASPBERRY_PI_CM1),
            ("CM3", boards.RASPBERRY_PI_CM3),
            ("CM4", boards.RASPBERRY_PI_CM4),
            ("CM5", boards.RASPBERRY_PI_CM5),
        ):
            with self.subTest(model=model):
                self.opened.clear()
                board = self.make_board(revision=None, model="Raspberry Pi " + model)
                self.assertEqual(board.id, expected)
                self.assertEqual(
                    self.opened,
                    [
                        "/etc/blinka-board",
                        "/proc/device-tree/system/linux,revision",
                    ],
                )

    def test_other_pi_models(self):
        self.file_error = FileNotFoundError()
        for revision, expected in (
            ("000e", boards.RASPBERRY_PI_B_REV2),
            ("a02082", boards.RASPBERRY_PI_3B),
            ("a03111", boards.RASPBERRY_PI_4B),
            ("d04170", boards.RASPBERRY_PI_5),
        ):
            with self.subTest(revision=revision):
                self.assertEqual(self.make_board(revision).id, expected)
        self.assertEqual(self.opened, ["/etc/blinka-board"] * 4)

    def test_unidentified_pi(self):
        self.contents = "UNKNOWN"
        self.assertIsNone(self.make_board(revision=None).id)
        self.assertEqual(
            self.opened,
            ["/etc/blinka-board", "/proc/device-tree/system/linux,revision"],
        )

    def test_non_pi_override(self):
        for chip_id, selected in (
            (chips.RK3566, boards.RADXA_CM3),
            (chips.A311D, boards.KHADAS_VIM3),
            (chips.AM33XX, boards.BEAGLEBONE_BLACK),
        ):
            with self.subTest(chip_id=chip_id):
                self.contents = selected
                board = self.make_board(chip_id=chip_id)
                self.assertEqual(board.id, selected)
                self.assertEqual(board.detector.chip.id, chip_id)
                board.detector.get_device_model.assert_not_called()

    def test_non_linux_platforms(self):
        for platform in ("darwin", "win32", "esp8266", "rp2"):
            with self.subTest(platform=platform):
                with patch("adafruit_platformdetect.board.sys.platform", platform):
                    board = self.make_board(chip_id=chips.OS_AGNOSTIC)
                    self.assertEqual(board.id, boards.OS_AGNOSTIC_BOARD)
        self.assertEqual(self.opened, [])

    def test_linux2_override(self):
        with patch("adafruit_platformdetect.board.sys.platform", "linux2"):
            self.assertEqual(self.make_board().id, boards.RASPBERRY_PI_4B)

    def test_unknown_chip_unchanged(self):
        board = self.make_board(chip_id=None)
        self.assertEqual(board.id, boards.RASPBERRY_PI_4B)
        self.assertIsNone(board.detector.chip.id)

    def test_non_pi_fallback(self):
        self.contents = "UNKNOWN"
        board = self.make_board(chip_id=chips.OS_AGNOSTIC)
        self.assertEqual(board.id, boards.OS_AGNOSTIC_BOARD)
        board.detector.get_cpuinfo_field.assert_not_called()
        self.assertEqual(self.opened, ["/etc/blinka-board"])

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
        self.assertEqual(self.opened, ["/etc/blinka-board"])

    def test_fallback_cached(self):
        self.contents = "UNKNOWN"
        board = self.make_board()
        self.assertEqual(board.id, boards.RASPBERRY_PI_CM4)
        self.contents = "RASPBERRY_PI_4B"
        self.assertEqual(board.id, boards.RASPBERRY_PI_CM4)
        self.assertEqual(self.opened, ["/etc/blinka-board"])

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

# SPDX-FileCopyrightText: 2022 Chris Wilson <christopher.david.wilson@gmail.com>
#
# SPDX-License-Identifier: MIT

"""
`adafruit_platformdetect.protocols`
================================================================================

Protocol definitions

* Author(s): Chris Wilson

Implementation Notes
--------------------

**Software and Dependencies:**

* Linux and Python 3.7 or Higher

"""

from typing import Optional

# Protocol was introduced in Python 3.8.
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol


class DetectorProtocol(Protocol):
    """Wrap various platform detection functions."""

    def get_cpuinfo_field(self, field: str) -> Optional[str]:
        """
        Search /proc/cpuinfo for a field and return its value, if found,
        otherwise None.
        """
        ...

    def check_dt_compatible_value(self, value: str) -> bool:
        """
        Search /proc/device-tree/compatible for a value and return True, if found,
        otherwise False.
        """
        ...

    def get_armbian_release_field(self, field: str) -> Optional[str]:
        """
        Search /etc/armbian-release, if it exists, for a field and return its
        value, if found, otherwise None.
        """
        ...

    def get_device_model(self) -> Optional[str]:
        """
        Search /proc/device-tree/model for the device model and return its value, if found,
        otherwise None.
        """
        ...

    def get_device_compatible(self) -> Optional[str]:
        """
        Search /proc/device-tree/compatible for the compatible chip name.
        """
        ...

    def check_board_asset_tag_value(self) -> Optional[str]:
        """
        Search /sys/devices/virtual/dmi/id for the device model and return its value, if found,
        otherwise None.
        """
        ...

    def check_board_name_value(self) -> Optional[str]:
        """
        Search /sys/devices/virtual/dmi/id for the board name and return its value, if found,
        otherwise None. Debian/ubuntu based
        """
        ...

# Copyright (c) 2014-2018 Adafruit Industries
# Author: Tony DiCola, Limor Fried, Brennen Bearnes

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Attempt to detect the current platform.
"""
import re

from adafruit_platformdetect.board import Board
from adafruit_platformdetect.chip import Chip


# Various methods here may retain state in future, so tell pylint not to worry
# that they don't use self right now:
# pylint: disable=no-self-use
class Detector:
    """Wrap various platform detection functions."""

    def __init__(self):
        self.board = Board(self)
        self.chip = Chip(self)

    def get_cpuinfo_field(self, field):
        """Get a given field value from cpuinfo.

        Read the file `/proc/cpuinfo` and look for a given
        field.

        Args:
            field (str): Field to look value of.

        Returns:
            Found value of given field, otherwise None.
        """
        # Match a line like 'Hardware   : BCM2709':
        pattern = r'^' + field + r'\s+:\s+(.*)$'

        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read().split('\n')

            for line in cpuinfo:
                match = re.search(pattern, line, flags=re.IGNORECASE)

                if match:
                    return match.group(1)

        return None

    def check_dt_compatible_value(self, value):
        """Check if value in device-tree compatible.

        Read the file `/proc/device-tree/compatible` and
        search for a value.

        Args1:
            value (str): Value to check on file.

        Returns:
            True if found, otherwise False.
        """
        # Match a value like 'qcom,apq8016-sbc':
        try:

            with open('/proc/device-tree/compatible') as compatible_file:

                if value in compatible_file.read():
                    return True

        except FileNotFoundError:
            pass

        return False

    def get_armbian_release_field(self, field):
        """Search the armbian release field.

        Read the content of the `/etc/armbian-release` if file
        exists.

        Args:
            field (str): Field to look value of.

        Returns:
            Release field if found, otherwise None.
        """
        field_value = None
        pattern = r'^' + field + r'=(.*)'
        try:

            with open("/etc/armbian-release", 'r') as release_file:
                armbian = release_file.read().split('\n')

                for line in armbian:
                    match = re.search(pattern, line)

                    if match:
                        field_value = match.group(1)
        except FileNotFoundError:
            pass

        return field_value

    def get_device_model(self):
        """Search for the device model.

        Read the content of `/proc/device-tree/model` and return its value.

        Returns:
            Device model if found, otherwise None
        """
        try:

            with open('/proc/device-tree/model', 'r') as model_file:
                model = model_file.read()
                return model

        except FileNotFoundError:
            pass

    def get_device_compatible(self):
        """Search for the compatible chip name.

        Read the content of the `/proc/device-tree/compatible` file.

        Returns:
            Compatible model found on file, otherwise None
        """


        try:

            with open('/proc/device-tree/compatible', 'r') as model_file:
                model = model_file.read()
                return model

        except FileNotFoundError:
            pass

    def _get_value(self, relationship, value):
        """Get a value from a relationship dictionary.

        When the key:value pair contains a function as a value,
        it will execute the function. In some cases the function
        is used to also get a value which could end up in a string.

        Args:
            relationship (dict): Relationship key:value
            value (str): Value to be look for in the relationship.

        Returns:
            Depending on the value assigned to a key.
        """
        gotten_value = relationship.get(value, None)

        if callable(gotten_value):
            final_value = gotten_value()

        elif isinstance(gotten_value, str) and gotten_value:
            final_value = gotten_value

        else:  # Not found.
            final_value = None

        return final_value

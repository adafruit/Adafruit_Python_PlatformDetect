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
import sys
import platform
import re
from adafruit_platformdetect.board import Board
from adafruit_platformdetect.chip import Chip

class PlatformDetect:

    def __init__(self):
        self.board = Board(self)
        self.chip = Chip(self)

    def cpuinfo_field(self, field):
        """
        Search /proc/cpuinfo for a field and return its value, if found,
        otherwise None.
        """
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read().split('\n')
            for line in cpuinfo:
                # Match a line like 'Hardware   : BCM2709':
                pattern = r'^' + field + r'\s+:\s+(.*)$'
                match = re.search(pattern, line, flags=re.IGNORECASE)
                if match:
                    return match.group(1)

        return None

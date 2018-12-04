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

class PlatformDetect:

    def is_raspberrypi(self):
        return true

    def is_linux(self):
        return true

    def pi_revision_code(self):
        """Detect the version of the Raspberry Pi.  Returns either 1, 2 or
        None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
        Raspberry Pi 2 (model B+), or not a Raspberry Pi.
        """
        # Check /proc/cpuinfo for the Hardware field value.
        # 2708 is Pi 1
        # 2709 is Pi 2
        # 2835 is Pi 3 (or greater) on 4.9.x kernel
        # Anything else is not a Pi.
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()
        # Match a line like 'Hardware   : BCM2709'
        match = re.search(r'^Hardware\s+:\s+(\w+)$', cpuinfo,
                          flags=re.MULTILINE | re.IGNORECASE)

        if not match:
            # Couldn't find the hardware, assume it isn't a pi.
            return None

        if match.group(1) not in ('BCM2708', 'BCM2709', 'BCM2835'):
            # Something else, not a pi.
            return None

        rev_match = re.search(r'^Revision\s+:\s+(\w+)$', cpuinfo,
                              flags=re.MULTILINE | re.IGNORECASE)
        if rev_match:
            return rev_match.group(1)

        return None

#   0002    B   1.0     256 MB  Egoman
#   0003    B   1.0     256 MB  Egoman
#   0004    B   2.0     256 MB  Sony UK
#   0005    B   2.0     256 MB  Qisda
#   0006    B   2.0     256 MB  Egoman
#   0007    A   2.0     256 MB  Egoman
#   0008    A   2.0     256 MB  Sony UK
#   0009    A   2.0     256 MB  Qisda
#   000d    B   2.0     512 MB  Egoman
#   000e    B   2.0     512 MB  Sony UK
#   000f    B   2.0     512 MB  Egoman
#   0010    B+  1.0     512 MB  Sony UK
#   0011    CM1     1.0     512 MB  Sony UK
#   0012    A+  1.1     256 MB  Sony UK
#   0013    B+  1.2     512 MB  Embest
#   0014    CM1     1.0     512 MB  Embest
#   0015    A+  1.1     256 MB / 512 MB     Embest

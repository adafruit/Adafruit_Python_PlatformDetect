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
#   0011    CM1 1.0     512 MB  Sony UK
#   0012    A+  1.1     256 MB  Sony UK
#   0013    B+  1.2     512 MB  Embest
#   0014    CM1 1.0     512 MB  Embest
#   0015    A+  1.1     256 MB / 512 MB Embest
#
#   900021  A+  1.1     512 MB  Sony UK
#   900032  B+  1.2     512 MB  Sony UK
#   900092  Zero    1.2     512 MB  Sony UK
#   920092  Zero    1.2     512 MB  Embest
#   900093  Zero    1.3     512 MB  Sony UK
#   9000c1  Zero W  1.1     512 MB  Sony UK
#   920093  Zero    1.3     512 MB  Embest
#   a01040  2B  1.0     1 GB    Sony UK
#   a01041  2B  1.1     1 GB    Sony UK
#   a02082  3B  1.2     1 GB    Sony UK
#   a020a0  CM3     1.0     1 GB    Sony UK
#   a21041  2B  1.1     1 GB    Embest
#   a22042  2B (with BCM2837)   1.2     1 GB    Embest
#   a22082  3B  1.2     1 GB    Embest
#   a32082  3B  1.2     1 GB    Sony Japan
#   a52082  3B  1.2     1 GB    Stadium
#   a020d3  3B+     1.3     1 GB    Sony UK
#   9020e0  3A+     1.0     512 MB  Sony UK

    @property
    def any_raspberry_pi(self):
        return self.pi_rev_code() is not None

    @property
    def raspberry_pi_b(self):
        return self.pi_rev_code() in (
            '0002', '0003', '0004', '0005', '0006',
            '000d', '000e', '000f'
        )

    @property
    def raspberry_pi_b_plus(self):
        return self.pi_rev_code() in ('0010', '0013', '900032')

    @property
    def raspberry_pi_a(self):
        return self.pi_rev_code() in ('0007', '0008', '0009')

    @property
    def raspberry_pi_a_plus(self):
        return self.pi_rev_code() in ('0012', '0015', '900021')

    @property
    def raspberry_pi_cm1(self):
        return self.pi_rev_code() in ('0011', '0014')

    @property
    def raspberry_pi_zero(self):
        return self.pi_rev_code() in ('900092', '920092', '900093', '920093')

    @property
    def raspberry_pi_zero_w(self):
        return self.pi_rev_code() in ('9000c1')

    @property
    def raspberry_pi_2b(self):
        return self.pi_rev_code() in ('a01040', 'a01041', 'a21041', 'a22042')

    @property
    def raspberry_pi_3b(self):
        return self.pi_rev_code() in ('a22082', 'a32082', 'a52082')

    @property
    def raspberrypi_3b_plus(self):
        return self.pi_rev_code() in ('a020d3')

    @property
    def raspberry_pi_cm3(self):
        return self.pi_rev_code() in ('a020a0')

    @property
    def raspberrypi_3a_plus(self):
        return self.pi_rev_code() in ('9020e0')

    def pi_rev_code(self):
        # 2708 is Pi 1
        # 2709 is Pi 2
        # 2835 is Pi 3 (or greater) on 4.9.x kernel
        # Anything else is not a Pi.

        if self.cpuinfo_field('Hardware') not in ('BCM2708', 'BCM2709', 'BCM2835'):
            # Something else, not a Pi.
            return None
        return self.cpuinfo_field('Revision')

    def cpuinfo_field(self, field):
        with open('/proc/cpuinfo', 'r') as infile:
            cpuinfo = infile.read()

        # Check /proc/cpuinfo for a field value.
        # Match a line like 'Hardware   : BCM2709'
        pattern = r'^' + field + r'\s+:\s+(\w+)$'
        match = re.search(pattern, cpuinfo, flags=re.MULTILINE | re.IGNORECASE)
        if match:
            return match.group(1)
        return None

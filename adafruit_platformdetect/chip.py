"""Attempt detection of current chip / CPU."""
import os
import sys

AM33XX = "AM33XX"
IMX8MX = "IMX8MX"
BCM2XXX = "BCM2XXX"
ESP8266 = "ESP8266"
SAMD21 = "SAMD21"
STM32 = "STM32"
SUN8I = "SUN8I"
S805 = "S805"
S905 = "S905"
S922X = "S922X"
SAMA5 = "SAMA5"
T210 = "T210"
T186 = "T186"
T194 = "T194"
APQ8016 = "APQ8016"
GENERIC_X86 = "GENERIC_X86"
FT232H = "FT232H"
HFU540 = "HFU540"
MCP2221 = "MCP2221"
BINHO = "BINHO"
MIPS24KC = "MIPS24KC"
MIPS24KEC = "MIPS24KEC"
A64 = "A64"

BCM_RANGE = {'BCM2708', 'BCM2709', 'BCM2835', 'BCM2837', 'bcm2708', 'bcm2709',
             'bcm2835', 'bcm2837'}


class Chip:
    """Attempt detection of current chip / CPU."""

    def __init__(self, detector):
        self.detector = detector

    @property
    def id(self):  # pylint: disable=invalid-name,too-many-branches,too-many-return-statements
        """Return a unique id for the detected chip, if any."""
        # There are some times we want to trick the platform detection
        # say if a raspberry pi doesn't have the right ID, or for testing
        try:
            return os.environ['BLINKA_FORCECHIP']
        except KeyError:  # no forced chip, continue with testing!
            pass

        # Special cases controlled by environment var
        if os.environ.get('BLINKA_FT232H'):
            from pyftdi.usbtools import UsbTools  # pylint: disable=import-error
            # look for it based on PID/VID
            count = len(UsbTools.find_all([(0x0403, 0x6014)]))
            if count == 0:
                raise RuntimeError('BLINKA_FT232H environment variable ' + \
                                   'set, but no FT232H device found')
            return FT232H
        if os.environ.get('BLINKA_MCP2221'):
            import hid  # pylint: disable=import-error
            # look for it based on PID/VID
            for dev in hid.enumerate():
                if dev['vendor_id'] == 0x04D8 and dev['product_id'] == 0x00DD:
                    return MCP2221
            raise RuntimeError('BLINKA_MCP2221 environment variable ' + \
                               'set, but no MCP2221 device found')
        if os.environ.get('BLINKA_NOVA'):
            return BINHO

        platform = sys.platform
        if platform in ('linux', 'linux2'):
            return self._linux_id()
        if platform == 'esp8266':
            return ESP8266
        if platform == 'samd21':
            return SAMD21
        if platform == 'pyboard':
            return STM32
        # nothing found!
        return None

    # pylint: enable=invalid-name

    def _linux_id(self):  # pylint: disable=too-many-branches,too-many-statements
        """Attempt to detect the CPU on a computer running the Linux kernel."""

        if self.detector.check_dt_compatible_value('qcom,apq8016'):
            return APQ8016

        if self.detector.check_dt_compatible_value('fu500'):
            return HFU540

        linux_id = None
        hardware = self.detector.get_cpuinfo_field('Hardware')

        if hardware is None:
            vendor_id = self.detector.get_cpuinfo_field('vendor_id')
            if vendor_id in ('GenuineIntel', 'AuthenticAMD'):
                linux_id = GENERIC_X86

            compatible = self.detector.get_device_compatible()
            if compatible and 'tegra' in compatible:
                if 'cv' in compatible or 'nano' in compatible:
                    linux_id = T210
                elif 'quill' in compatible:
                    linux_id = T186
                elif 'xavier' in compatible:
                    linux_id = T194
            if compatible and 'imx8m' in compatible:
                linux_id = IMX8MX
            if compatible and 'odroid-c2' in compatible:
                linux_id = S905
            if compatible and 'amlogic, g12b' in compatible:
                linux_id = S922X

            cpu_model = self.detector.get_cpuinfo_field("cpu model")

            if cpu_model is not None:
                if "MIPS 24Kc" in cpu_model:
                    linux_id = MIPS24KC
                elif "MIPS 24KEc" in cpu_model:
                    linux_id = MIPS24KEC

            # we still haven't identified the hardware, so
            # convert it to a list and let the remaining
            # conditions attempt.
            if not linux_id:
                hardware = [
                    entry.replace('\x00', '') for entry in compatible.split(',')
                ]

        if not linux_id:
            if 'AM33XX' in hardware:
                linux_id = AM33XX
            elif 'sun8i' in hardware:
                linux_id = SUN8I
            elif 'ODROIDC' in hardware:
                linux_id = S805
            elif 'ODROID-C2' in hardware:
                linux_id = S905
            elif 'ODROID-N2' in hardware:
                linux_id = S922X
            elif 'SAMA5' in hardware:
                linux_id = SAMA5
            elif "Pinebook" in hardware:
                linux_id = A64
            elif "sun50iw1p1" in hardware:
                linux_id = A64
            else:
                if isinstance(hardware, str):
                    if hardware in BCM_RANGE:
                        linux_id = BCM2XXX
                elif isinstance(hardware, list):
                    if set(hardware) & BCM_RANGE:
                        linux_id = BCM2XXX

        return linux_id

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected chip.  See
        list of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

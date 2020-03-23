"""Attempt detection of current chip / CPU."""
import os
import sys

from adafruit_platformdetect.constants import chips


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
            return chips.FT232H
        if os.environ.get('BLINKA_MCP2221'):
            import hid  # pylint: disable=import-error
            # look for it based on PID/VID
            for dev in hid.enumerate():
                if dev['vendor_id'] == 0x04D8 and dev['product_id'] == 0x00DD:
                    return chips.MCP2221
            raise RuntimeError('BLINKA_MCP2221 environment variable ' + \
                               'set, but no MCP2221 device found')
        if os.environ.get('BLINKA_NOVA'):
            return chips.BINHO

        platform = sys.platform
        if platform in ('linux', 'linux2'):
            return self._linux_id()
        if platform == 'esp8266':
            return chips.ESP8266
        if platform == 'samd21':
            return chips.SAMD21
        if platform == 'pyboard':
            return chips.STM32
        # nothing found!
        return None

    # pylint: enable=invalid-name

    def _linux_id(self):  # pylint: disable=too-many-branches,too-many-statements
        """Attempt to detect the CPU on a computer running the Linux kernel."""

        if self.detector.check_dt_compatible_value('qcom,apq8016'):
            return chips.APQ8016

        if self.detector.check_dt_compatible_value('fu500'):
            return chips.HFU540

        linux_id = None
        hardware = self.detector.get_cpuinfo_field('Hardware')

        if hardware is None:
            vendor_id = self.detector.get_cpuinfo_field('vendor_id')
            if vendor_id in ('GenuineIntel', 'AuthenticAMD'):
                linux_id = chips.GENERIC_X86

            compatible = self.detector.get_device_compatible()
            if compatible and 'tegra' in compatible:
                compats = compatible.split('\x00')
                if 'nvidia,tegra210' in compats:
                    linux_id = chips.T210
                elif 'nvidia,tegra186' in compats:
                    linux_id = chips.T186
                elif 'nvidia,tegra194' in compats:
                    linux_id = chips.T194
            if compatible and 'imx8m' in compatible:
                linux_id = chips.IMX8MX
            if compatible and 'odroid-c2' in compatible:
                linux_id = chips.S905
            if compatible and 'amlogic, g12a' in compatible:
                linux_id = chips.S905X3
            if compatible and 'amlogic, g12b' in compatible:
                linux_id = chips.S922X
            if compatible and 'sun50i-a64' in compatible:
                linux_id = chips.A64

            cpu_model = self.detector.get_cpuinfo_field("cpu model")

            if cpu_model is not None:
                if "MIPS 24Kc" in cpu_model:
                    linux_id = chips.MIPS24KC
                elif "MIPS 24KEc" in cpu_model:
                    linux_id = chips.MIPS24KEC

            # we still haven't identified the hardware, so
            # convert it to a list and let the remaining
            # conditions attempt.
            if not linux_id:
                hardware = [
                    entry.replace('\x00', '') for entry in compatible.split(',')
                ]

        if not linux_id:
            if 'AM33XX' in hardware:
                linux_id = chips.AM33XX
            elif 'sun8i' in hardware:
                linux_id = chips.SUN8I
            elif 'ODROIDC' in hardware:
                linux_id = chips.S805
            elif 'ODROID-C2' in hardware:
                linux_id = chips.S905
            elif 'ODROID-N2' in hardware:
                linux_id = chips.S922X
            elif 'ODROID-C4' in hardware:
                linux_id = chips.S905X3
            elif 'SAMA5' in hardware:
                linux_id = chips.SAMA5
            elif "Pinebook" in hardware:
                linux_id = chips.A64
            elif "sun50iw1p1" in hardware:
                linux_id = chips.A64
            elif "Xilinx Zynq" in hardware:
                compatible = self.detector.get_device_compatible()
                if compatible and 'xlnx,zynq-7000' in compatible:
                    linux_id = chips.ZYNQ7000
            else:
                if isinstance(hardware, str):
                    if hardware.upper() in chips.BCM_RANGE:
                        linux_id = chips.BCM2XXX
                elif isinstance(hardware, list):
                    if set([model.upper() for model in hardware]) & chips.BCM_RANGE:
                        linux_id = chips.BCM2XXX

        return linux_id

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected chip.  See
        list of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

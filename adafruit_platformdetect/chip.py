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
                raise RuntimeError(
                    'BLINKA_FT232H environment variable set, but no FT232H device found'
                )
            return chips.FT232H
        if os.environ.get('BLINKA_MCP2221'):

            import hid  # pylint: disable=import-error
            # look for it based on PID/VID
            for dev in hid.enumerate():

                if dev['vendor_id'] == 0x04D8 and dev['product_id'] == 0x00DD:
                    return chips.MCP2221

            raise RuntimeError(
                'BLINKA_MCP2221 environment variable set, but no MCP2221 device found'
            )
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
            # Relationship compatible-chip
            compatible_chips = {
                'cv':               chips.T210,
                'nano':             chips.T210,
                'quill':            chips.T186,
                'xavier':           chips.T194,
                'imx8m':            chips.IMX8MX,
                'odroid-c2':        chips.S905,
                'amlogic, g12b':    chips.S922X

            }

            if compatible:

                for compatible_value in compatible_chips:

                    if compatible_value in compatible:
                        linux_id = compatible_chips[compatible_value]
                        break

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
            # Relationship hardware-chip
            hardware_chips = {
                'AM33XX':       chips.AM33XX,
                'sun8i':        chips.SUN8I,
                'ODROIDC':      chips.S805,
                'ODROID-C2':    chips.S905,
                'ODROID-N2':    chips.S922X,
                'SAMA5':        chips.SAMA5,
                "Pinebook":     chips.A64,
                "sun50iw1p1":   chips.A64,
            }

            for hardware_value in hardware_chips:

                if hardware_value in hardware:
                    # return found value
                    linux_id = hardware_chips[hardware_value]
                    break

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

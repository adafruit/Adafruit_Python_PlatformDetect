"""Attempt detection of current chip / CPU."""
import sys
import os

AM33XX = "AM33XX"
IMX8MX = "IMX8MX"
BCM2XXX = "BCM2XXX"
ESP8266 = "ESP8266"
SAMD21 = "SAMD21"
STM32 = "STM32"
SUN8I = "SUN8I"
S805 = "S805"
S905 = "S905"
SAMA5 = "SAMA5"
T210 = "T210"
T186 = "T186"
T194 = "T194"
GENERIC_X86 = "GENERIC_X86"
FT232H = "FT232H"

class Chip:
    """Attempt detection of current chip / CPU."""
    def __init__(self, detector):
        self.detector = detector

    @property
    def id(self): # pylint: disable=invalid-name,too-many-branches,too-many-return-statements
        """Return a unique id for the detected chip, if any."""
        # There are some times we want to trick the platform detection
        # say if a raspberry pi doesn't have the right ID, or for testing
        try:
            return os.environ['BLINKA_FORCECHIP']
        except KeyError: # no forced chip, continue with testing!
            pass

        # Special case, if we have an environment var set, we could use FT232H
        try:
            if os.environ['BLINKA_FT232H']:
                # we can't have ftdi1 as a dependency cause its wierd
                # to install, sigh.
                import ftdi1 as ftdi # pylint: disable=import-error
                try:
                    ctx = None
                    ctx = ftdi.new()  # Create a libftdi context.
                    # Enumerate FTDI devices.
                    count, _ = ftdi.usb_find_all(ctx, 0, 0)
                    if count < 0:
                        raise RuntimeError('ftdi_usb_find_all returned error %d : %s' %
                                           count, ftdi.get_error_string(self._ctx))
                    if count == 0:
                        raise RuntimeError('BLINKA_FT232H environment variable' + \
                                           'set, but no FT232H device found')
                finally:
                    # Make sure to clean up list and context when done.
                    if ctx is not None:
                        ftdi.free(ctx)
            return FT232H
        except KeyError: # no FT232H environment var
            pass

        platform = sys.platform
        if platform == "linux" or platform == "linux2":
            return self._linux_id()
        if platform == "esp8266":
            return ESP8266
        if platform == "samd21":
            return SAMD21
        if platform == "pyboard":
            return STM32
        # nothing found!
        return None
    # pylint: enable=invalid-name

    def _linux_id(self): # pylint: disable=too-many-branches
        """Attempt to detect the CPU on a computer running the Linux kernel."""
        linux_id = None

        hardware = self.detector.get_cpuinfo_field("Hardware")

        if hardware is None:
            vendor_id = self.detector.get_cpuinfo_field("vendor_id")
            if vendor_id in ("GenuineIntel", "AuthenticAMD"):
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

        elif hardware in ("BCM2708", "BCM2709", "BCM2835"):
            linux_id = BCM2XXX
        elif "AM33XX" in hardware:
            linux_id = AM33XX
        elif "sun8i" in hardware:
            linux_id = SUN8I
        elif "ODROIDC" in hardware:
            linux_id = S805
        elif "ODROID-C2" in hardware:
            linux_id = S905
        elif "SAMA5" in hardware:
            linux_id = SAMA5

        return linux_id

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected chip.  See
        list of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

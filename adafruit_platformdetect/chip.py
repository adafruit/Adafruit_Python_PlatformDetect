"""Attempt detection of current chip / CPU."""
import sys

AM33XX = "AM33XX"
BCM2XXX = "BCM2XXX"
ESP8266 = "ESP8266"
SAMD21 = "SAMD21"
STM32 = "STM32"
SUN8I = "SUN8I"
GENERIC_X86 = "GENERIC_X86"

class Chip:
    """Attempt detection of current chip / CPU."""
    def __init__(self, detector):
        self.detector = detector

    @property
    # pylint: disable=invalid-name
    def id(self):
        """Return a unique id for the detected chip, if any."""
        platform = sys.platform
        if platform == "linux":
            return self._linux_id()
        if platform == "esp8266":
            return ESP8266
        if platform == "samd21":
            return SAMD21
        if platform == "pyboard":
            return STM32
        return None
    # pylint: enable=invalid-name

    def _linux_id(self):
        """Attempt to detect the CPU on a computer running the Linux kernel."""
        linux_id = None

        hardware = self.detector.get_cpuinfo_field("Hardware")

        if hardware is None:
            vendor_id = self.detector.get_cpuinfo_field("vendor_id")
            if vendor_id in ("GenuineIntel", "AuthenticAMD"):
                linux_id = GENERIC_X86
        elif hardware in ("BCM2708", "BCM2708", "BCM2835"):
            linux_id = BCM2XXX
        elif "AM33XX" in hardware:
            linux_id = AM33XX
        elif "sun8i" in hardware:
            linux_id = SUN8I

        return linux_id

    def __getattr__(self, attr):
        """
        Detect whether the given attribute is the currently-detected chip.  See
        list of constants at the top of this module for available options.
        """
        if self.id == attr:
            return True
        return False

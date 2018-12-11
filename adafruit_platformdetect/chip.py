import sys

AM33XX = "AM33XX"
BCM2XXX = "BCM2XXX"
ESP8266 = "ESP8266"
SAMD21 = "SAMD21"
STM32 = "STM32"
SUN8I = "SUN8I"

class Chip:
    """Attempt detection of current chip / CPU."""
    def __init__(self, detect):
        self.detect = detect

    @property
    def id(self):
        platform = sys.platform
        if platform == "linux":
            return self._linux_id()
        elif platform == "esp8266":
            return ESP8266
        elif platform == "samd21":
            return SAMD21
        elif platform == "pyboard":
            return STM32
        else:
            return None

    def _linux_id(self):
        """Attempt to detect the CPU on a computer running the Linux kernel."""
        id = None

        hardware = self.detect.get_cpuinfo_field("Hardware")
        if hardware in ('BCM2708', 'BCM2708', 'BCM2835'):
            id = BCM2XXX
        elif "AM33XX" in hardwarename:
            id = AM33XX
        elif "sun8i" in hardwarename:
            id = SUN8I

        return id

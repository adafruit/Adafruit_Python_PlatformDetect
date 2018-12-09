import sys

ESP8266 = "esp8266",
SAMD21 = "samd21",
STM32 = "stm32",

class Chip:
    def __init__(self, detect):
        self.detect = detect

    @property
    def name(self):
        name = None

        platform = sys.platform
        if platform is not None:
            if platform == "esp8266":
                name = ESP8266
            elif platform == "samd21":
                name = SAMD21
            elif platform == "pyboard":
                name = STM32
            elif platform == "linux":
                # XXX: Here is where some work to detect ARM / x86 stuff for
                # real needs to happen.
                hardwarename = self.detect.cpuinfo_field("Hardware")
                if not hardwarename:
                    return None
                if "sun8i" in hardwarename:
                    name = "sun8i"
                else:
                    name = hardwarename

        return name

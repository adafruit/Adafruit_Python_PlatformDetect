from adafruit_platformdetect import PlatformDetect

detect = PlatformDetect()

print(detect.pi_revision_code())

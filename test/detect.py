import adafruit_platformdetect

detect = adafruit_platformdetect.PlatformDetect()
print(detect.board.name)

# print(adafruit_platformdetect.board.RASPBERRY_PI_B)

print(detect.board.pi_rev_code)
print(detect.board.any_raspberry_pi)

print(detect.board.raspberry_pi_3b_plus)
print(detect.board.raspberry_pi_a)
print(detect.board.raspberry_pi_3b_plus)
print(detect.board.raspberry_pi_a)

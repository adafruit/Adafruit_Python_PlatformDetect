# Pi revision codes from:
#   https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md

RASPBERRY_PI_B = "raspberry_pi_b"
RASPBERRY_PI_B_PLUS = "raspberry_pi_b_plus"
RASPBERRY_PI_A = "raspberry_pi_a"
RASPBERRY_PI_A_PLUS = "raspberry_pi_a_plus"
RASPBERRY_PI_CM1 = "raspberry_pi_cm1"
RASPBERRY_PI_ZERO = "raspberry_pi_zero"
RASPBERRY_PI_ZERO_W = "raspberry_pi_zero_w"
RASPBERRY_PI_2B = "raspberry_pi_2b"
RASPBERRY_PI_3B = "raspberry_pi_3b"
RASPBERRY_PI_3B_PLUS = "raspberry_pi_3b_plus"
RASPBERRY_PI_CM3 = "raspberry_pi_cm3"
RASPBERRY_PI_3A_PLUS = "raspberry_pi_3a_plus"

_PI_REV_CODES = {
    RASPBERRY_PI_B: ('0002', '0003', '0004', '0005', '0006', '000d', '000e', '000f'),
    RASPBERRY_PI_B_PLUS: ('0010', '0013', '900032'),
    RASPBERRY_PI_A: ('0007', '0008', '0009'),
    RASPBERRY_PI_A_PLUS: ('0012', '0015', '900021'),
    RASPBERRY_PI_CM1: ('0011', '0014'),
    RASPBERRY_PI_ZERO: ('900092', '920092', '900093', '920093'),
    RASPBERRY_PI_ZERO_W: ('9000c1',),
    RASPBERRY_PI_2B: ('a01040', 'a01041', 'a21041', 'a22042'),
    RASPBERRY_PI_3B: ('a22082', 'a32082', 'a52082'),
    RASPBERRY_PI_3B_PLUS: ('a020d3',),
    RASPBERRY_PI_CM3: ('a020a0',),
    RASPBERRY_PI_3A_PLUS: ('9020e0',),
}

class Board:
    def __init__(self, detect):
        self.detect = detect

    def __getattr__(self, attr):
        # Check Raspberry Pi values:
        if attr in _PI_REV_CODES:
            return self.pi_rev_code in _PI_REV_CODES[attr]

        raise AttributeError(attr + " is not a defined board")

    @property
    def name(self):
        name = None

        pi_rev_code = self.pi_rev_code
        if pi_rev_code:
            for model, codes in _PI_REV_CODES.items():
                if pi_rev_code in codes:
                    name = model
                    break

        return name

    @property
    def any_raspberry_pi(self):
        return self.pi_rev_code is not None

    @property
    def pi_rev_code(self):
        # 2708 is Pi 1
        # 2709 is Pi 2
        # 2835 is Pi 3 (or greater) on 4.9.x kernel
        # Anything else is not a Pi.

        if self.detect.cpuinfo_field('Hardware') not in ('BCM2708', 'BCM2709', 'BCM2835'):
            # Something else, not a Pi.
            return None
        return self.detect.cpuinfo_field('Revision')

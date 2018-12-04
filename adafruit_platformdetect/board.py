# Pi revision codes:
# 0002   | B              | 1.0 | 256 MB          | Egoman
# 0003   | B              | 1.0 | 256 MB          | Egoman
# 0004   | B              | 2.0 | 256 MB          | Sony UK
# 0005   | B              | 2.0 | 256 MB          | Qisda
# 0006   | B              | 2.0 | 256 MB          | Egoman
# 0007   | A              | 2.0 | 256 MB          | Egoman
# 0008   | A              | 2.0 | 256 MB          | Sony UK
# 0009   | A              | 2.0 | 256 MB          | Qisda
# 000d   | B              | 2.0 | 512 MB          | Egoman
# 000e   | B              | 2.0 | 512 MB          | Sony UK
# 000f   | B              | 2.0 | 512 MB          | Egoman
# 0010   | B+             | 1.0 | 512 MB          | Sony UK
# 0011   | CM1            | 1.0 | 512 MB          | Sony UK
# 0012   | A+             | 1.1 | 256 MB          | Sony UK
# 0013   | B+             | 1.2 | 512 MB          | Embest
# 0014   | CM1            | 1.0 | 512 MB          | Embest
# 0015   | A+             | 1.1 | 256 MB / 512 MB | Embest
# 900021 | A+             | 1.1 | 512 MB          | Sony UK
# 900032 | B+             | 1.2 | 512 MB          | Sony UK
# 900092 | Zero           | 1.2 | 512 MB          | Sony UK
# 920092 | Zero           | 1.2 | 512 MB          | Embest
# 900093 | Zero           | 1.3 | 512 MB          | Sony UK
# 9000c1 | Zero W         | 1.1 | 512 MB          | Sony UK
# 920093 | Zero           | 1.3 | 512 MB          | Embest
# a01040 | 2B             | 1.0 | 1 GB            | Sony UK
# a01041 | 2B             | 1.1 | 1 GB            | Sony UK
# a02082 | 3B             | 1.2 | 1 GB            | Sony UK
# a020a0 | CM3            | 1.0 | 1 GB            | Sony UK
# a21041 | 2B             | 1.1 | 1 GB            | Embest
# a22042 | 2B (w/BCM2837) | 1.2 | 1 GB            | Embest
# a22082 | 3B             | 1.2 | 1 GB            | Embest
# a32082 | 3B             | 1.2 | 1 GB            | Sony Japan
# a52082 | 3B             | 1.2 | 1 GB            | Stadium
# a020d3 | 3B+            | 1.3 | 1 GB            | Sony UK
# 9020e0 | 3A+            | 1.0 | 512 MB          | Sony UK

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
        pi_rev_code = self.pi_rev_code
        name = None
        if pi_rev_code:
            for model, codes in _PI_REV_CODES:
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
        return self.cpuinfo_field('Revision')

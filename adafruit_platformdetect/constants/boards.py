"""Definition of boards and/or ids"""
# Allow for aligned constant definitions:
# pylint: disable=bad-whitespace
BEAGLEBONE = "BEAGLEBONE"
BEAGLEBONE_BLACK = "BEAGLEBONE_BLACK"
BEAGLEBONE_BLUE = "BEAGLEBONE_BLUE"
BEAGLEBONE_BLACK_WIRELESS = "BEAGLEBONE_BLACK_WIRELESS"
BEAGLEBONE_POCKETBEAGLE = "BEAGLEBONE_POCKETBEAGLE"
BEAGLEBONE_GREEN = "BEAGLEBONE_GREEN"
BEAGLEBONE_GREEN_WIRELESS = "BEAGLEBONE_GREEN_WIRELESS"
BEAGLEBONE_BLACK_INDUSTRIAL = "BEAGLEBONE_BLACK_INDUSTRIAL"
BEAGLEBONE_ENHANCED = "BEAGLEBONE_ENHANCED"
BEAGLEBONE_USOMIQ = "BEAGLEBONE_USOMIQ"
BEAGLEBONE_AIR = "BEAGLEBONE_AIR"
BEAGLEBONE_POCKETBONE = "BEAGLEBONE_POCKETBONE"
BEAGLELOGIC_STANDALONE = "BEAGLELOGIC_STANDALONE"
OSD3358_DEV_BOARD = "OSD3358_DEV_BOARD"
OSD3358_SM_RED = "OSD3358_SM_RED"

FEATHER_HUZZAH = "FEATHER_HUZZAH"
FEATHER_M0_EXPRESS = "FEATHER_M0_EXPRESS"
GENERIC_LINUX_PC = "GENERIC_LINUX_PC"
PYBOARD = "PYBOARD"
NODEMCU = "NODEMCU"
GIANT_BOARD = "GIANT_BOARD"

# Clockwork Pi boards
CLOCKWORK_CPI3 = "CLOCKWORK_CPI3"

# Orange Pi boards
ORANGE_PI_PC = "ORANGE_PI_PC"
ORANGE_PI_R1 = "ORANGE_PI_R1"
ORANGE_PI_ZERO = "ORANGE_PI_ZERO"
ORANGE_PI_ONE = "ORANGE_PI_ONE"
ORANGE_PI_LITE = "ORANGE_PI_LITE"
ORANGE_PI_PC_PLUS = "ORANGE_PI_PC_PLUS"
ORANGE_PI_PLUS_2E = "ORANGE_PI_PLUS_2E"
ORANGE_PI_2 = "ORANGE_PI_2"

# NVIDIA Jetson boards
JETSON_TX1 = "JETSON_TX1"
JETSON_TX2 = "JETSON_TX2"
JETSON_XAVIER = "JETSON_XAVIER"
JETSON_NANO = "JETSON_NANO"
JETSON_NX = "JETSON_NX"

# Google Coral dev board
CORAL_EDGE_TPU_DEV = "CORAL_EDGE_TPU_DEV"

# Xilinx PYNQ FPGA dev boards
PYNQ_Z1 = "PYNQ_Z1"
PYNQ_Z2 = "PYNQ_Z2"

# Various Raspberry Pi models
RASPBERRY_PI_B_REV1 = "RASPBERRY_PI_B_REV1"
RASPBERRY_PI_B_REV2 = "RASPBERRY_PI_B_REV2"
RASPBERRY_PI_B_PLUS = "RASPBERRY_PI_B_PLUS"
RASPBERRY_PI_A = "RASPBERRY_PI_A"
RASPBERRY_PI_A_PLUS = "RASPBERRY_PI_A_PLUS"
RASPBERRY_PI_CM1 = "RASPBERRY_PI_CM1"
RASPBERRY_PI_ZERO = "RASPBERRY_PI_ZERO"
RASPBERRY_PI_ZERO_W = "RASPBERRY_PI_ZERO_W"
RASPBERRY_PI_2B = "RASPBERRY_PI_2B"
RASPBERRY_PI_3B = "RASPBERRY_PI_3B"
RASPBERRY_PI_3B_PLUS = "RASPBERRY_PI_3B_PLUS"
RASPBERRY_PI_CM3 = "RASPBERRY_PI_CM3"
RASPBERRY_PI_3A_PLUS = "RASPBERRY_PI_3A_PLUS"
RASPBERRY_PI_CM3_PLUS = "RASPBERRY_PI_CM3_PLUS"
RASPBERRY_PI_4B = "RASPBERRY_PI_4B"
RASPBERRY_PI_AVNET_IIOT_GW = "RASPBERY_PI_AVNET_IIOT_GW"

ODROID_C1 = "ODROID_C1"
ODROID_C1_PLUS = "ODROID_C1_PLUS"
ODROID_C2 = "ODROID_C2"
ODROID_C4 = "ODROID_C4"
ODROID_N2 = "ODROID_N2"
ODROID_XU4 = "ODROID_XU4"

FTDI_FT232H = "FTDI_FT232H"
DRAGONBOARD_410C = "DRAGONBOARD_410C"

SIFIVE_UNLEASHED = "SIFIVE_UNLEASHED"

MICROCHIP_MCP2221 = "MICROCHIP_MCP2221"

BINHO_NOVA = "BINHO_NOVA"

ONION_OMEGA = "ONION_OMEGA"
ONION_OMEGA2 = "ONION_OMEGA2"

PINE64 = "PINE64"
PINEBOOK = "PINEBOOK"
PINEPHONE = "PINEPHONE"

ROCK_PI_S = "ROCK_PI_S"

GREATFET_ONE = "GREATFET_ONE"
UDOO_BOLT_V3 = "UDOO_BOLT_V3"
UDOO_BOLT_V8 = "UDOO_BOLT_V8"

# pylint: enable=bad-whitespace

# OrangePI
_ORANGE_PI_IDS = (
    ORANGE_PI_PC,
    ORANGE_PI_R1,
    ORANGE_PI_ZERO,
    ORANGE_PI_ONE,
    ORANGE_PI_LITE,
    ORANGE_PI_PC_PLUS,
    ORANGE_PI_PLUS_2E,
    ORANGE_PI_2,
)

_CORAL_IDS = (CORAL_EDGE_TPU_DEV,)

_PYNQ_IDS = (
    PYNQ_Z1,
    PYNQ_Z2,
)

_JETSON_IDS = {
    JETSON_TX1: ("nvidia,p2371-2180", "nvidia,jetson-cv",),
    JETSON_TX2: (
        "nvidia,p2771-0000",
        "nvidia,p2771-0888",
        "nvidia,p3489-0000",
        "nvidia,lightning",
        "nvidia,quill",
        "nvidia,storm",
    ),
    JETSON_XAVIER: ("nvidia,p2972-0000", "nvidia,p2972-0006", "nvidia,jetson-xavier",),
    JETSON_NANO: ("nvidia,p3450-0000", "nvidia,p3450-0002", "nvidia,jetson-nano",),
    JETSON_NX: (
        "nvidia,p3509-0000+p3668-0000",
        "nvidia,p3509-0000+p3668-0001",
        "nvidia,p3449-0000+p3668-0000",
        "nvidia,p3449-0000+p3668-0001",
    ),
}

_RASPBERRY_PI_40_PIN_IDS = (
    RASPBERRY_PI_B_PLUS,
    RASPBERRY_PI_A_PLUS,
    RASPBERRY_PI_ZERO,
    RASPBERRY_PI_ZERO_W,
    RASPBERRY_PI_2B,
    RASPBERRY_PI_3B,
    RASPBERRY_PI_3B_PLUS,
    RASPBERRY_PI_3A_PLUS,
    RASPBERRY_PI_4B,
    RASPBERRY_PI_AVNET_IIOT_GW,
)

_RASPBERRY_PI_CM_IDS = (RASPBERRY_PI_CM1, RASPBERRY_PI_CM3, RASPBERRY_PI_CM3_PLUS)

_ODROID_40_PIN_IDS = (
    ODROID_C1,
    ODROID_C1_PLUS,
    ODROID_C2,
    ODROID_C4,
    ODROID_N2,
    ODROID_XU4,
)

_BEAGLEBONE_IDS = (
    BEAGLEBONE,
    BEAGLEBONE_BLACK,
    BEAGLEBONE_BLUE,
    BEAGLEBONE_BLACK_WIRELESS,
    BEAGLEBONE_POCKETBEAGLE,
    BEAGLEBONE_GREEN,
    BEAGLEBONE_GREEN_WIRELESS,
    BEAGLEBONE_BLACK_INDUSTRIAL,
    BEAGLEBONE_ENHANCED,
    BEAGLEBONE_USOMIQ,
    BEAGLEBONE_AIR,
    BEAGLEBONE_POCKETBONE,
    BEAGLELOGIC_STANDALONE,
    OSD3358_DEV_BOARD,
    OSD3358_SM_RED,
)

_LINARO_96BOARDS_IDS = (DRAGONBOARD_410C,)

_SIFIVE_IDS = (SIFIVE_UNLEASHED,)

# BeagleBone eeprom board ids from:
#   https://github.com/beagleboard/image-builder
# Thanks to zmatt on freenode #beagle for pointers.
_BEAGLEBONE_BOARD_IDS = {
    # Original bone/white:
    BEAGLEBONE: (
        ("A4", "A335BONE00A4"),
        ("A5", "A335BONE00A5"),
        ("A6", "A335BONE00A6"),
        ("A6A", "A335BONE0A6A"),
        ("A6B", "A335BONE0A6B"),
        ("B", "A335BONE000B"),
    ),
    BEAGLEBONE_BLACK: (
        ("A5", "A335BNLT00A5"),
        ("A5A", "A335BNLT0A5A"),
        ("A5B", "A335BNLT0A5B"),
        ("A5C", "A335BNLT0A5C"),
        ("A6", "A335BNLT00A6"),
        ("B", "A335BNLT000B"),
        ("C", "A335BNLT000C"),
        ("C", "A335BNLT00C0"),
    ),
    BEAGLEBONE_BLUE: (("A2", "A335BNLTBLA2"),),
    BEAGLEBONE_BLACK_WIRELESS: (("A5", "A335BNLTBWA5"),),
    BEAGLEBONE_POCKETBEAGLE: (("A2", "A335PBGL00A2"),),
    BEAGLEBONE_GREEN: (("1A", "A335BNLT...."), ("UNKNOWN", "A335BNLTBBG1"),),
    BEAGLEBONE_GREEN_WIRELESS: (("W1A", "A335BNLTGW1A"),),
    BEAGLEBONE_BLACK_INDUSTRIAL: (
        ("A0", "A335BNLTAIA0"),  # Arrow
        ("A0", "A335BNLTEIA0"),  # Element14
    ),
    BEAGLEBONE_ENHANCED: (("A", "A335BNLTSE0A"),),
    BEAGLEBONE_USOMIQ: (("6", "A335BNLTME06"),),
    BEAGLEBONE_AIR: (("A0", "A335BNLTNAD0"),),
    BEAGLEBONE_POCKETBONE: (("0", "A335BNLTBP00"),),
    OSD3358_DEV_BOARD: (("0.1", "A335BNLTGH01"),),
    OSD3358_SM_RED: (("0", "A335BNLTOS00"),),
    BEAGLELOGIC_STANDALONE: (("A", "A335BLGC000A"),),
}

# Pi revision codes from:
#   https://www.raspberrypi.org/documentation/hardware/raspberrypi/revision-codes/README.md

# Each tuple here contains both the base codes, and the versions that indicate
# the Pi is overvolted / overclocked - for 4-digit codes, this will be prefixed
# with 1000, and for 6-digit codes it'll be prefixed with 1.  These are placed
# on separate lines.

_PI_REV_CODES = {
    RASPBERRY_PI_B_REV1: (
        # Regular codes:
        "0002",
        "0003",
        # Overvolted/clocked versions:
        "1000002",
        "1000003",
    ),
    RASPBERRY_PI_B_REV2: (
        "0005",
        "0006",
        "000d",
        "000e",
        "000f",
        "1000005",
        "1000006",
        "100000d",
        "100000e",
        "100000f",
    ),
    RASPBERRY_PI_B_PLUS: ("0010", "0013", "900032", "1000010", "1000013", "1900032",),
    RASPBERRY_PI_A: ("0007", "0008", "0009", "1000007", "1000008", "1000009",),
    RASPBERRY_PI_A_PLUS: ("0012", "0015", "900021", "1000012", "1000015", "1900021",),
    RASPBERRY_PI_CM1: ("0011", "0014", "10000011", "10000014",),
    RASPBERRY_PI_ZERO: (
        "900092",
        "920092",
        "900093",
        "920093",
        "1900092",
        "1920092",
        "1900093",
        "1920093",  # warranty bit 24
        "2900092",
        "2920092",
        "2900093",
        "2920093",  # warranty bit 25
    ),
    RASPBERRY_PI_ZERO_W: ("9000c1", "19000c1", "29000c1",),  # warranty bits
    RASPBERRY_PI_2B: (
        "a01040",
        "a01041",
        "a21041",
        "a22042",
        "1a01040",
        "1a01041",
        "1a21041",
        "1a22042",  # warranty bit 24
        "2a01040",
        "2a01041",
        "2a21041",
        "2a22042",  # warranty bit 25
        "3a01040",
        "3a01041",
        "3a21041",
        "3a22042",
    ),
    RASPBERRY_PI_3B: (
        "a02082",
        "a22082",
        "a32082",
        "a52082",
        "1a02082",
        "1a22082",
        "1a32082",
        "1a52082",  # warranty bit 24
        "2a02082",
        "2a22082",
        "2a32082",
        "2a52082",  # warranty bit 25
    ),
    RASPBERRY_PI_3B_PLUS: ("a020d3", "1a020d3", "2a020d3",),  # warranty bits
    RASPBERRY_PI_AVNET_IIOT_GW: ("60a220b0",),
    RASPBERRY_PI_CM3: (
        "a020a0",
        "a220a0",
        "1a020a0",
        "2a020a0",  # warranty bits
        "1a220a0",
        "2a220a0",
    ),
    RASPBERRY_PI_3A_PLUS: ("9020e0", "19020e0", "29020e0",),  # warranty bits
    RASPBERRY_PI_CM3_PLUS: ("a02100", "1a02100", "2a02100",),  # warranty bits
    RASPBERRY_PI_4B: (
        "a03111",
        "b03111",
        "c03111",
        "a03112",
        "b03112",
        "c03112",
        "1a03111",
        "2a03111",
        "1b03111",
        "2b03111",  # warranty bits
        "1c03111",
        "2c03111",
        "1a03112",
        "2a03112",
        "1b03112",
        "2b03112",
        "1c03112",
        "2c03112",
    ),
}

# Onion omega boards
_ONION_OMEGA_BOARD_IDS = (
    ONION_OMEGA,
    ONION_OMEGA2,
)

# Pine64 boards and devices
_PINE64_DEV_IDS = (PINE64, PINEBOOK, PINEPHONE)

# UDOO
_UDOO_BOARD_IDS = {UDOO_BOLT_V8: ("SC40-2000-0000-C0|C",)}

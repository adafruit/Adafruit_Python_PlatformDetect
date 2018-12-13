Introduction
============

This library provides best-guess platform detection for a range of single-board
computers and (potentially) other platforms.  It's intended for use in
`Adafruit_Blinka <https://github.com/adafruit/Adafruit_Blinka>`_, but may be
useful in other contexts.

The API is currently unstable and may change drastically in future releases.

Installation
============

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-motorkit/>`_. To install for current user:

.. code-block:: shell

    pip3 install Adafruit-PlatformDetect

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install Adafruit-PlatformDetect

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install Adafruit-PlatformDetect

Usage
=====

.. code-block:: python

    from adafruit_platformdetect import Detector
    detector = Detector()
    print("Chip id: ", detector.chip.id)
    print("Board id: ", detector.board.id)

    # Check for specific board models:
    print("Pi 3B+? ", detector.board.RASPBERRY_PI_3B_PLUS)
    print("BBB? ", detector.board.BEAGLEBONE_BLACK)
    print("Orange Pi PC? ", detector.board.ORANGE_PI_PC)
    print("generic Linux PC? ", detector.board.GENERIC_LINUX_PC)

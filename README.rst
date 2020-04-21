Introduction
============

.. image:: https://readthedocs.org/projects/Adafruit-PlatformDetect/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/platformdetect/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_PlatformDetect/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_PlatformDetect/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

This library provides best-guess platform detection for a range of single-board
computers and (potentially) other platforms.  It was written primarily for use
in `Adafruit_Blinka <https://github.com/adafruit/Adafruit_Blinka>`_, but may be
useful in other contexts.

Platform detection is divided into "chip" and "board" detection, with the latter
generally dependent on the former.  Platform info is gathered from:

  - Python's `sys.platform`

  - Various files on Linux systems:

    - /proc/cpuinfo (for processor info, Raspberry Pi hardware revisions, etc.)

    - /proc/device-tree/compatible (for 96Boards info)

  - Beaglebone EEPROM board IDs

  - Distribution-specific files such as /etc/armbian-release.

  Dependencies
  =============
  This driver depends on:

  * `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

  Please ensure all dependencies are available on the CircuitPython filesystem.
  This is easily achieved by downloading
  `the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

  Installing from PyPI
  =====================
  .. note:: This library is not available on PyPI yet. Install documentation is included
     as a standard element. Stay tuned for PyPI availability!

  .. todo:: Remove the above note if PyPI version is/will be available at time of release.
     If the library is not planned for PyPI, remove the entire 'Installing from PyPI' section.

  On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
  PyPI <https://pypi.org/project/Adafruit-PlatformDetect/>`_. To install for current user:

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

  Usage Example
  =============

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

  Contributing
  ============

  Contributions are welcome! Please read our `Code of Conduct
  <https://github.com/adafruit/Adafruit_CircuitPython_PlatformDetect/blob/master/CODE_OF_CONDUCT.md>`_
  before contributing to help this project stay welcoming.

  Documentation
  =============

  For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
  

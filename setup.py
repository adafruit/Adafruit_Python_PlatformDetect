#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='Adafruit-PlatformDetect',
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description='Platform detection for use by libraries like Adafruit-Blinka.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Adafruit Industries',
    author_email='circuitpython@adafruit.com',
    python_requires='>=3.4.0',
    url='https://github.com/adafruit/Adafruit_Python_PlatformDetect',

    # If your package is a single module, use this instead of 'packages':
    packages=['adafruit_platformdetect'],

    install_requires=[],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: MicroPython',
    ],
)

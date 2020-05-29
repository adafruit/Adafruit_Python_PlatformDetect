"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Adafruit-PlatformDetect",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Platform detection for use by libraries like Adafruit-Blinka.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    python_requires=">=3.5.0",
    url="https://github.com/adafruit/Adafruit_Python_PlatformDetect",
    # If your package is a single module, use this instead of 'packages':
    author="Adafruit Industries",
    author_email="circuitpython@adafruit.com",
    install_requires=[],
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    packages=["adafruit_platformdetect", "adafruit_platformdetect.constants"],
)

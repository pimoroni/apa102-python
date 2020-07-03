# APA102 Library

[![Build Status](https://travis-ci.com/pimoroni/apa102-python.svg?branch=master)](https://travis-ci.com/pimoroni/apa102-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/apa102-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/apa102-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/apa102.svg)](https://pypi.python.org/pypi/apa102)
[![Python Versions](https://img.shields.io/pypi/pyversions/apa102.svg)](https://pypi.python.org/pypi/apa102)

# Pre-requisites

You must enable SPI:

* spi: `sudo raspi-config nonint do_spi 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

Stable library from PyPi:

* Just run `python3 -m pip install apa102`

Latest/development library from GitHub:

* `git clone https://github.com/pimoroni/apa102-python`
* `cd apa102-python`
* `sudo ./install.sh`


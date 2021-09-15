# APA102 Library

[![Build Status](https://travis-ci.com/pimoroni/apa102-python.svg?branch=master)](https://travis-ci.com/pimoroni/apa102-python)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/apa102-python/badge.svg?branch=master)](https://coveralls.io/github/pimoroni/apa102-python?branch=master)
[![PyPi Package](https://img.shields.io/pypi/v/apa102.svg)](https://pypi.python.org/pypi/apa102)
[![Python Versions](https://img.shields.io/pypi/pyversions/apa102.svg)](https://pypi.python.org/pypi/apa102)

A simple library to drive APA102 pixels from the Raspberry Pi, or similar SBCs.

Uses either spidev or RPi.GPIO depending on the pins specified.

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

# Usage

The APA102 class will attempt to use spidev or RPi.GPIO depending on which pins you specify.

For example; three RGB LEDs connected to SPI pins 10 and 11 with chip-select 8 (CE0):

```python
from apa102 import APA102
lights = APA102(3, 10, 11, 8)
```

You can then set individual pixels with `set_pixel`:

```
lights.set_pixel(0, 255, 0, 0)  # Pixel 1 to Red
lights.set_pixel(1, 0, 255, 0)  # Pixel 2 to Green
lights.set_pixel(2, 0, 0, 255)  # Pixel 3 to Blue
```

Pixels are zero-indexed and accept Red, Green and Blue colour values from 0 to 255.

To set the lights, after the colours were set as wanted, use the `show` method:

```python
lights.show()
```

Without the `show` method, only the internal data is updated, the lights changes only after this function call.

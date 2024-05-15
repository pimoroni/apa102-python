# APA102 Library

[![Build Status](https://img.shields.io/github/actions/workflow/status/pimoroni/apa102-python/test.yml?branch=main)](https://github.com/pimoroni/apa102-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/pimoroni/apa102-python/badge.svg?branch=main)](https://coveralls.io/github/pimoroni/apa102-python?branch=main)
[![PyPi Package](https://img.shields.io/pypi/v/apa102.svg)](https://pypi.python.org/pypi/apa102)
[![Python Versions](https://img.shields.io/pypi/pyversions/apa102.svg)](https://pypi.python.org/pypi/apa102)

A simple library to drive APA102 pixels from the Raspberry Pi, or compatible SBCs.

Uses either spidev or gpiod depending on the pins specified.

# Pre-requisites

You must enable SPI:

* spi: `sudo raspi-config nonint do_spi 0`

You can optionally run `sudo raspi-config` or the graphical Raspberry Pi Configuration UI to enable interfaces.

# Installing

## Stable library from PyPi:

```
git clone https://github.com/pimoroni/apa102-python
cd apa102-python
./install.sh
```

### Latest/development library from GitHub:

```
git clone https://github.com/pimoroni/apa102-python
cd apa102-python
./install.sh --unstable
```

## Manual Install

If you've already set up a virtual environment and just want to grab the library:

```
pip install apa102
```

# Usage

The APA102 class will attempt to use spidev or gpiod depending on which pins you specify.

:warning: You should prefer SPI if you have control over the pins- gpiod on a Pi is a *slow* way to bitbang SPI.

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

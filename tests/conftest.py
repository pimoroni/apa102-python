"""Test configuration.

These allow the mocking of various Python modules
that might otherwise have runtime side-effects.
"""
import sys

import mock
import pytest


@pytest.fixture(scope='function', autouse=True)
def cleanup_apa102():
    yield None
    del sys.modules['apa102']


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    gpiochip = mock.MagicMock()
    gpiochip.line_offset_from_id = lambda x: x
    gpiod = mock.MagicMock()
    gpiod.Value.INACTIVE = False
    gpiod.Value.ACTIVE = True
    sys.modules['gpiod'] = gpiod
    sys.modules['gpiod.line'] = mock.MagicMock()
    sys.modules['gpiodevice'] = mock.MagicMock()
    sys.modules['gpiodevice'].find_chip_by_platform.return_value = gpiochip
    yield gpiod, gpiochip
    del sys.modules['gpiod']
    del sys.modules['gpiod.line']
    del sys.modules['gpiodevice']


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock Spidev module."""

    spidev = mock.MagicMock()

    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']

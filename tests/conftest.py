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

    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['gpiod'] = mock.MagicMock()
    sys.modules['gpiodevice'] = mock.MagicMock()
    yield GPIO
    del sys.modules['gpiod']
    del sys.modules['gpiodevice']


@pytest.fixture(scope='function', autouse=False)
def spidev():
    """Mock Spidev module."""

    spidev = mock.MagicMock()

    sys.modules['spidev'] = spidev
    yield spidev
    del sys.modules['spidev']

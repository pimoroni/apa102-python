import time

import gpiod
import gpiodevice
import spidev
from gpiod.line import Direction, Value

__version__ = '0.0.3'


class APA102():
    def __init__(self, count=1, gpio_data=14, gpio_clock=15, gpio_cs=None, brightness=1.0, force_gpio=False, invert=False, spi_max_speed_hz=1000000):
        """Initialise an APA102 device.

        Will use SPI if it's available on the specified data/clock pins.

        :param count: Number of individual RGB LEDs
        :param gpio_data: BCM pin for data
        :param gpio_clock: BCM pin for clock
        :param gpio_cs: BCM pin for chip-select
        :param force_gpio: Specify true to force use of GPIO bitbanging

        """

        self._invert = invert

        self._gpio_lines = None

        if invert:
            # TODO Add invert support for SPI
            force_gpio = True

        self._gpio = None
        self._gpio_cs = None
        self._gpio_data = None
        self._gpio_clock = None
        self._spi = None
        self._brightness = brightness

        self._sof_length = 4  # SOF bytes
        self._eof_length = 4  # EOF bytes
        buffer_length = count * 4

        self._buf = []

        for _ in range(self._sof_length):
            self._buf.append(0b00000000)

        self._buf += [0b11100000 | int(self._brightness * 31) for _ in range(buffer_length)]

        for _ in range(self._eof_length):
            self._buf.append(0b11111111)

        if not force_gpio and gpio_data == 10 and gpio_clock == 11 and gpio_cs in (None, 7, 8):
            cs_channel = 0
            if gpio_cs is not None:
                cs_channel = [8, 7].index(gpio_cs)
            self._spi = spidev.SpiDev(0, cs_channel)
            self._spi.max_speed_hz = spi_max_speed_hz
            if gpio_cs is None:
                self._spi.no_cs = True

        elif not force_gpio and gpio_data == 20 and gpio_clock == 21 and gpio_cs in (None, 18, 17, 16):
            cs_channel = 0
            if gpio_cs is not None:
                cs_channel = [18, 17, 16].index(gpio_cs)
            self._spi = spidev.SpiDev(0, cs_channel)
            self._spi.max_speed_hz = spi_max_speed_hz
            if gpio_cs is None:
                self._spi.no_cs = True

        else:
            gpio = gpiodevice.find_chip_by_platform()
            pins = {"data": gpio_data, "clock": gpio_clock}
            if gpio_cs is not None:
                pins["chip-select"] = gpio_cs
            gpiodevice.check_pins_available(gpio, pins)
            self._gpio_data = gpio.line_offset_from_id(gpio_data)
            self._gpio_clock = gpio.line_offset_from_id(gpio_clock)
            config = {
                self._gpio_data: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE if self._invert else Value.INACTIVE),
                self._gpio_clock: gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.ACTIVE if self._invert else Value.INACTIVE)
            }
            if gpio_cs is not None:
                self._gpio_cs = gpio.line_offset_from_id(gpio_cs)
                config[self._gpio_cs] = gpiod.LineSettings(direction=Direction.OUTPUT, output_value=Value.INACTIVE)

            self._gpio_lines = gpio.request_lines(consumer="apa102", config=config)

    def _write_byte(self, byte):
        for _ in range(8):
            bit = not (byte & 0x80) if self._invert else (byte & 0x80)
            self._gpio_lines.set_value(self._gpio_data, Value.ACTIVE if bit else Value.INACTIVE)
            self._gpio_lines.set_value(self._gpio_clock, Value.INACTIVE if self._invert else Value.ACTIVE)
            time.sleep(0)
            byte <<= 1
            self._gpio_lines.set_value(self._gpio_clock, Value.ACTIVE if self._invert else Value.INACTIVE)
            time.sleep(0)

    def set_pixel(self, x, r, g, b):
        """Set a single pixel

        :param x: x index of pixel
        :param r: amount of red (0 to 255)
        :param g: amount of green (0 to 255)
        :param b: amount of blue (0 to 255)

        """
        offset = self._sof_length + (x * 4) + 1
        self._buf[offset:offset + 3] = [b, g, r]

    def set_brightness(self, x, brightness):
        """Set global brightness of a single pixel

        :param x: x index of pixel
        :param brightness: LED brightness (0.0 to 1.0)

        """
        offset = self._sof_length + (x * 4)
        self._buf[offset] = 0b11100000 | int(31 * brightness)

    def show(self):
        """Display the buffer

        Outputs the buffer to connected LEDs using either bitbanged GPIO or SPI.

        """
        if self._gpio_cs is not None:
            self._gpio_lines.set_value(self._gpio_cs, Value.INACTIVE)

        if self._spi is not None:
            self._spi.xfer3(self._buf)

        else:
            for byte in self._buf:
                self._write_byte(byte)

        if self._gpio_cs is not None:
            self._gpio_lines.set_value(self._gpio_cs, Value.ACTIVE)

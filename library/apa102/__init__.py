import time
import spidev
import RPi.GPIO as GPIO

__version__ = '0.0.1'


class APA102():
    def __init__(self, count=1, gpio_data=14, gpio_clock=15, gpio_cs=None, brightness=1.0, force_gpio=False):
        """Initialise an APA102 device.

        Will use SPI if it's available on the specified data/clock pins.

        :param pixel_count: Number of individual RGB LEDs
        :param gpio_data: BCM pin for data
        :param gpio_clock: BCM pin for clock
        :param gpio_cs: BCM pin for chip-select
        :param force_gpio: Specify true to force use of GPIO bitbanging

        """

        self._gpio_clock = gpio_clock
        self._gpio_data = gpio_data
        self._gpio_cs = gpio_cs

        self._brightness = brightness

        self._sof_length = 8 * 8  # SOF bytes
        self._eof_length = 8 * 4  # EOF bytes
        buffer_length = count * 4
        buffer_length += self._sof_length
        buffer_length += self._eof_length

        self._buf = []

        for _ in range(self._sof_length):
            self._buf.append(0b00000000)

        self._buf += [0b11100000 | int(self._brightness * 31) for _ in range(buffer_length)]

        for _ in range(self._eof_length):
            self._buf.append(0b11111111)

        if not force_gpio and gpio_data == 10 and gpio_clock == 11 and gpio_cs in (7, 8):
            self._spi = spidev.SpiDev(0, [8, 7].index(gpio_cs))
            self._gpio_cs = None

        elif not force_gpio and gpio_data == 20 and gpio_clock == 21 and gpio_cs in (18, 17, 16):
            self._spi = spidev.SpiDev(0, [18, 17, 16].index(gpio_cs))
            self._gpio_cs = None

        else:
            if gpio is None:
                self._gpio = GPIO
                self._gpio.setmode(GPIO.BCM)
                self._gpio.setup([gpio_data, gpio_clock], GPIO.OUT)

    def _write_byte(self, byte):
        for _ in range(8):
            self._gpio.output(self._gpio_data, byte & 0x80)
            self._gpio.output(self._gpio_clock, 1)
            time.sleep(0)
            byte <<= 1
            self._gpio.output(self._gpio_clock, 0)
            time.sleep(0)

    def set_pixel(self, x, r, g, b):
        """Set a single pixel

        :param x: x index of pixel
        :param r: amount of red (0 to 255)
        :param g: amount of green (0 to 255)
        :param b: amount of blue (0 to 255)

        """
        offset = self._sof_length + (x * 4) + 1
        self._buf[offset:offset + 3] = [r, g, b]

    def set_brightness(self, x, brightness):
        """Set global brightness of a single pixel

        :param x: x index of pixel
        :param brightness: LED brightness (0.0 to 1.0)

        """
        offset = self._sof_length + (x * 4)
        self._buf[offset] = int(31 * brightness)

    def show(self):
        """Display the buffer

        Outputs the buffer to connected LEDs using either bitbanged GPIO or SPI.

        """
        if self._gpio_cs is not None:
            self._gpio.output(self._gpio_cs, 0)

        if self._spi is not None:
            self._spi.xfer3(self._buf)

        else:
            for byte in self._buf:
                self._write_byte(byte)

        if self._gpio_cs is not None:
            self._gpio.output(self._gpio_cs, 1)

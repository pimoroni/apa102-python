import mock


def test_show_spi(GPIO, spidev):
    import apa102

    lights = apa102.APA102(3, 10, 11, 8)

    spidev.SpiDev.assert_has_calls((
        mock.call(0, 0),
    ))

    lights.set_pixel(0, 255, 0, 0)
    lights.set_pixel(1, 0, 255, 0)
    lights.set_pixel(2, 0, 0, 255)

    lights.show()

    spidev.SpiDev(0, 0).xfer3.assert_has_calls((
        mock.call(lights._buf),
    ))

    del lights

def test_show_gpio(GPIO, spidev):
    import apa102

    lights = apa102.APA102(3, 10, 11, 8, force_gpio=True)

    lights.set_pixel(0, 255, 0, 0)
    lights.set_pixel(1, 0, 255, 0)
    lights.set_pixel(2, 0, 0, 255)

    lights.show()

    assert GPIO.output.call_count == 4898  # Count of pin transitions

    del lights
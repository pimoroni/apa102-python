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

    assert lights._gpio_lines.set_value.call_count == 162   # Count of clock pin transitions + chip-select
    assert lights._gpio_lines.set_values.call_count == 160  # Count of clock pin transitions + data pin

    # Should match, since we have two transitions per clock pulse. Must discount the chip-select wiggle though.
    assert lights._gpio_lines.set_values.call_count == lights._gpio_lines.set_value.call_count - 2

    del lights

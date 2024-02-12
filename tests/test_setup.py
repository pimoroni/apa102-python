import mock


def test_setup_spi(GPIO, spidev):
    import apa102

    lights = apa102.APA102(3, 10, 11, 8)

    spidev.SpiDev.assert_has_calls((
        mock.call(0, 0),
    ))

    del lights


def test_setup_gpio(GPIO, spidev):
    import apa102

    gpiod, gpiochip = GPIO

    lights = apa102.APA102(3, 2, 3, 4)

    gpiochip.request_lines.assert_has_calls((
        mock.call(consumer="apa102", config={
            2: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE),
            3: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE),
            4: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)
        }),
    ))

    del lights


def test_setup_gpio_inverted(GPIO, spidev):
    import apa102

    gpiod, gpiochip = GPIO

    lights = apa102.APA102(3, 2, 3, 4, invert=True)

    gpiochip.request_lines.assert_has_calls((
        mock.call(consumer="apa102", config={
            2: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.ACTIVE),
            3: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.ACTIVE),
            4: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)
        }),
    ))

    del lights


def test_setup_force_gpio(GPIO, spidev):
    import apa102

    gpiod, gpiochip = GPIO

    lights = apa102.APA102(3, 10, 11, 8, force_gpio=True)

    gpiochip.request_lines.assert_has_calls((
        mock.call(consumer="apa102", config={
            10: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE),
            11: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE),
            8: gpiod.LineSettings(direction=gpiod.Direction.OUTPUT, output_value=gpiod.Value.INACTIVE)
        }),
    ))

    del lights

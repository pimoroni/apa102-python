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

    lights = apa102.APA102(3, 2, 3, 4)

    GPIO.setmode.assert_has_calls((
        mock.call(GPIO.BCM),
    ))

    GPIO.setup.assert_has_calls((
        mock.call(2, GPIO.OUT, initial=0),
        mock.call(3, GPIO.OUT, initial=0),
        mock.call(4, GPIO.OUT)
    ))

    del lights


def test_setup_gpio_inverted(GPIO, spidev):
    import apa102

    lights = apa102.APA102(3, 2, 3, 4, invert=True)

    GPIO.setmode.assert_has_calls((
        mock.call(GPIO.BCM),
    ))

    GPIO.setup.assert_has_calls((
        mock.call(2, GPIO.OUT, initial=1),
        mock.call(3, GPIO.OUT, initial=1),
        mock.call(4, GPIO.OUT)
    ))

    del lights


def test_setup_force_gpio(GPIO, spidev):
    import apa102

    lights = apa102.APA102(3, 10, 11, 8, force_gpio=True)

    GPIO.setmode.assert_has_calls((
        mock.call(GPIO.BCM),
    ))

    GPIO.setup.assert_has_calls((
        mock.call(10, GPIO.OUT, initial=0),
        mock.call(11, GPIO.OUT, initial=0),
        mock.call(8, GPIO.OUT)
    ))

    del lights

import time

from apa102 import APA102

"""

This example should show Red, Purple, Blue, Teal, Green, Yellow in sequence.

Swap PIN_DAT and PIN_CLK for "Plasma" connector on Picade HAT

"""


NUM_LEDS = 4 * 4 * 4
PIN_DAT = 14
PIN_CLK = 15
PIN_SEL = None

colors = [
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255),
    (255, 0, 255)
]

lights = APA102(NUM_LEDS, PIN_DAT, PIN_CLK, PIN_SEL, brightness=0.5)

while True:
    for p in range(NUM_LEDS):
        lights.set_pixel(p, *colors[0])
    colors.insert(0, colors.pop(-1))
    lights.show()
    time.sleep(1.0)


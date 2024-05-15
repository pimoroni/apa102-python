import time
from colorsys import hsv_to_rgb

from apa102 import APA102

"""

This example should display a rainbow scaled across your LEDs.

Swap PIN_DAT and PIN_CLK for "Plasma" connector on Picade HAT

"""


NUM_LEDS = 4 * 4 * 4
FPS = 30
PIN_DAT = 14
PIN_CLK = 15
PIN_SEL = None


lights = APA102(NUM_LEDS, PIN_DAT, PIN_CLK, PIN_SEL, brightness=0.5)

total = NUM_LEDS // 4

while True:
    t = time.time() / 2
    for p in range(NUM_LEDS):
        offset = p // 4
        r, g, b = [int(c * 255) for c in hsv_to_rgb(t + offset / total, 1.0, 1.0)]
        lights.set_pixel(p, r, g, b)
    lights.show()
    time.sleep(1.0 / FPS)


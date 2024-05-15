import math
import time
from colorsys import hsv_to_rgb

from apa102 import APA102

"""

This example should show gently flowing up/down VU bars on pHAT BEAT.

Forgive liberal use of the spread "*" operator here...

"""


NUM_LEDS = 8 * 2
PIN_DAT = 23
PIN_CLK = 24
PIN_SEL = None

def to_rgb8(*col):
    return [int(c * 255) for c in col]

SPECTRUM = [to_rgb8(*hsv_to_rgb(n / 8 / 2, 1.0, 1.0)) for n in range(8, 0, -1)]


lights = APA102(NUM_LEDS, PIN_DAT, PIN_CLK, PIN_SEL, brightness=0.1)

while True:
    t = time.time() * 2.0
    # Create sin/cos waves scaled 0 to 8 (8 LEDs per bar)
    left = (math.sin(t) + 1.0) * 4.0
    right = (math.cos(t) + 1.0) * 4.0

    # Based on the values calculated above, set each pixel that should be
    # full on, and scale the brightness of the last pixel to the remainder.
    for p in range(8):
        bl = max(0.0, min(1.0, left))
        br = max(0.0, min(1.0, right))

        lights.set_pixel(p + 8, *[int(c * bl) for c in SPECTRUM[p]])
        lights.set_pixel(7 - p, *[int(c * br) for c in SPECTRUM[p]])

        left -= 1.0
        right -= 1.0

    lights.show()
    time.sleep(1.0 / 30.0)


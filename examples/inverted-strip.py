import time
from apa102 import APA102
from colorsys import hsv_to_rgb

lights = APA102(120, 5, 6, None, brightness=0.5, invert=True)

while True:
    t = time.time() * 0.1
    for x in range(120):
        h = t + (x / 240.0)
        r, g, b = [int(c * 255) for c in hsv_to_rgb(h, 1.0, 1.0)]
        lights.set_pixel(x, r, g, b)

    lights.show()
    time.sleep(1.0 / 60)

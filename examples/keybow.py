import time
from apa102 import APA102

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255)
]

lights = APA102(3, 10, 11, 8)

while True:
    a, b, c = colors
    lights.set_pixel(0, *a)
    lights.set_pixel(1, *b)
    lights.set_pixel(2, *c)
    lights.show()

    colors.insert(0, colors.pop(2))

    time.sleep(1.0)


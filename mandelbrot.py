from __future__ import print_function, unicode_literals, division
from PIL import Image
import sys
import math


class Mandelbrot(object):
    def __init__(self, (left, top), (right, bottom)):
        self.start = (left, top)
        self.end = (right, bottom)

    def map(self, width, height, x, y):
        left, top = self.start
        right, bottom = self.end
        return complex(
            left + (right - left) * ((x + 0.5) / width),
            top - (top - bottom) * ((y + 0.5) / height)
        )

    def iterate(self, z):
        iterations = 1000
        c = z
        for i in range(iterations):
            z = z ** 2 + c
            mag = z.real * z.real + z.imag * z.imag
            if mag >= 4:
                p = 255 - int(255 * (math.log(i + 1) /
                    math.log(iterations)))
                return (p, p, p)
        return (0, 0, 0)

    def draw_to(self, image):
        width, height = image.size
        for x in range(width):
            for y in range(height):
                zc = self.map(width, height, x, y)
                colour = self.iterate(zc)
                image.putpixel((x, y), colour)


if __name__ == "__main__":
    m = Mandelbrot((-2.5, 1.5), (1.5, -1.5))
    im = Image.new('RGB', (1024, 768))
    m.draw_to(im)
    if len(sys.argv) > 1:
        im.save(open(sys.argv[1], 'w'), 'PNG')

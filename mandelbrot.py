from __future__ import print_function, unicode_literals, division
from PIL import Image
import sys
import math


class Mandelbrot(object):
    def __init__(self, (left, top), (right, bottom)):
        self.start = (left, top)
        self.end = (right, bottom)

    def iterate(self, z):
        iterations = 1000
        c = z
        for i in range(iterations):
            z = z ** 2 + c
            mag = z.real * z.real + z.imag * z.imag
            if mag >= 4:
                return self.hsv(i, iterations)
        return (0, 0, 0)

    def greyscale(self, iteration, iterations):
        p = 255 - int(255 * (math.log(iteration + 1) /
            math.log(iterations)))
        return (p, p, p)

    def hsv(self, iteration, iterations):
        h = (1 - (math.log(iteration+1) / math.log(iterations))) * 6
        c = 0.5
        x = c * (1 - abs(h % 2 - 1))
        m = 0.3
        if 0 <= h < 1:
            rgb = (c, x, 0)
        elif 1 <= h < 2:
            rgb = (x, c, 0)
        elif 2 <= h < 3:
            rgb = (0, c, x)
        elif 3 <= h < 4:
            rgb = (0, x, c)
        elif 4 <= h < 5:
            rgb = (x, 0, c)
        else:
            rgb = (c, 0, x)
        return tuple(int(256 * (m+p)) for p in rgb)

    def draw_to(self, image):
        width, height = image.size
        left, top = self.start
        right, bottom = self.end
        for x in range(width):
            for y in range(height):
                zc = complex(
                    left + (right - left) * ((x + 0.5) / width),
                    top - (top - bottom) * ((y + 0.5) / height)
                )
                colour = self.iterate(zc)
                image.putpixel((x, y), colour)


if __name__ == "__main__":
    m = Mandelbrot((-2.5, 1.5), (1.5, -1.5))
    im = Image.new('RGB', (1024, 768))
    m.draw_to(im)
    if len(sys.argv) > 1:
        im.save(open(sys.argv[1], 'w'), 'PNG')

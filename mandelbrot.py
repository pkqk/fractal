from __future__ import print_function, unicode_literals, division

from PIL import Image, PngImagePlugin
import sys
import math
import random
from timeit import timeit


LOG2 = math.log(2)


class Mandelbrot(object):
    def __init__(self, left_top, right_bottom, iterations=30):
        self.start = left_top
        self.end = right_bottom
        self.iterations = iterations

    def in_cardoid_or_p2(self, z):
        q = (z.real - 1/4)**2 + z.imag**2
        if q * (q + ( z.real - 1/4)) < (y**2/4):
            return True
        return (z.real + 1)**2 + z.imag**2 < 1/16

    def iterate(self, z, colour_func):
        c = z
        if self.in_cardoid_or_p2(z):
            return (0, 0, 0)
        for i in range(self.iterations):
            z = (z * z) + c
            mag = z.real * z.real + z.imag * z.imag

            if mag >= 4:
                return colour_func(i, self.iterations, math.sqrt(mag))
        return (0, 0, 0)

    def greyscale(self, iteration, iterations, point):
        p = 255 - int(255 * (math.log(iteration + 1) /
            math.log(iterations)))
        return (p, p, p)

    def hsv(self, iteration, iterations, abs_point):
        h = 3*(iteration - math.log(math.log(abs_point))/LOG2)/iterations
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
                colour = self.iterate(zc, self.hsv)
                image.putpixel((x, y), colour)


if __name__ == "__main__":
    x, y, span = -1.3, 0.15, 0.4
    print(x,y,span)
    def gen():
        tl = (x - span, y + span)
        br = (x + span, y - span)
        m = Mandelbrot(tl, br, 40)
        im = Image.new('RGB', (200, 200))
        m.draw_to(im)
        if len(sys.argv) > 1:
            meta = PngImagePlugin.PngInfo()
            meta.add_text('mandelbrot', "top-left %s bottom-right %s iterations %s" % (tl, br, m.iterations), 0)
            im.save(open(sys.argv[1], 'w'), 'PNG', pnginfo=meta)
    print("time", timeit(gen, number=1))

import cmath
import math


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


def rotate_point(point, angle_degrees):
    """Rotate point around 0:0, with help of complex numbers"""
    rad = angle_degrees * math.pi / 180
    cangle = cmath.exp(rad * 1j)

    # calculate current angle relative to initial angle
    offset = complex(0, 0)
    v = cangle * (complex(point.x, point.y) - offset) + offset

    return Point(v.real, v.imag)

import cmath
import math


class Point:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


def rotate_point(point, angle_degrees):
    """Rotate point around 0:0, with help of complex numbers"""
    rad = angle_degrees * math.pi / 180
    cangle = cmath.exp(rad * 1j)

    # calculate current angle relative to initial angle
    offset = complex(0, 0)
    v = cangle * (complex(point.x, point.y) - offset) + offset

    return Point(v.real, v.imag)


# def cartesian_to_polar(x, y):
#     magnitude = np.sqrt(x ** 2 + y ** 2)
#     rad = np.arctan2(y, x)
#     return (magnitude, rad)


def polar_to_cartesian(magnitude, angle_degree):
    rad = angle_degree * math.pi / 180

    x = magnitude * math.cos(rad)
    y = magnitude * math.sin(rad)
    return Point(round(x, 2), round(y, 2))

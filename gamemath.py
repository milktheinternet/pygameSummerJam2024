from math import sqrt, sin, cos, pi, tau
from random import random


class Vector:
    def __init__(self, x=0.0, y: float | int = 0.0):
        self.set(x, y)

    def set(self, x=0.0, y: float | int = 0.0):
        if isinstance(x, list) or isinstance(x, tuple):
            self.x, self.y = x
        elif isinstance(x, int) or isinstance(x, float):
            self.x, self.y = x, y
        else:
            self.x, self.y = x.x, x.y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x, self.y-other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x*other.x, self.y*other.y)
        else:
            return Vector(self.x*other, self.y*other)

    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x/other.x, self.y/other.y)
        else:
            return Vector(self.x/other, self.y/other)

    @staticmethod
    def random():
        return Vector(random(), random())

    def __round__(self, n=None):
        return Vector(round(self.x, n), round(self.y, n))

    @property
    def tuple(self):
        return self.x, self.y

    @property
    def dist(self):
        return sqrt(self.x**2 + self.y**2)


def trim_angle_vec(angle: Vector):
    while angle.x < -pi:
        angle.x += tau
    while angle.x > pi:
        angle.x -= tau
    while angle.y < -pi:
        angle.y += tau
    while angle.y > pi:
        angle.y -= tau
    return angle


def angle_to_3d(angle: Vector):
    x = sin(angle.x) * cos(angle.y)
    y = sin(angle.y) * cos(angle.x)
    z = cos(angle.x) * cos(angle.y)
    return x, y, z


def to_screen(angle: Vector, display):
    fov = 1  # Field of view

    x, y, z = angle_to_3d(angle)

    if cos(angle.x)<0 or cos(angle.y)<0:
        return None  # Point is behind the camera

    minres = min(display.res.tuple)

    return Vector(int(((x / z) * fov) * minres),
                  int(((y / z) * fov) * minres)) + display.res/2
import pygame as pg
from gamemath import Vector


def gen_planet(size: Vector, humidity=1.0, temperature=0.5):
    srf = pg.Surface(size.tuple)
    water = (0, 0, 255)
    land = (200, 150, 100)
    radius = size.x/2
    pg.draw.circle(srf, water, (size/2).tuple, radius)
    return srf
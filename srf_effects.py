import pygame as pg
from random import randint


def scanlines(srf, nlines_range=(3,10), x_range=(-5, 5)):

    w, h = srf.get_size()
    def get_x():return randint(*x_range)
    def n_lines():return randint(*nlines_range)

    y = 0
    while y < h:
        nl = n_lines()
        if y + nl > h:
            nl = h - y
        x = get_x()
        srf2 = srf.subsurface(0, y, w, nl).copy()
        srf.blit(srf2, (x, y))
        y += nl

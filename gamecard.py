import pygame as pg
from random import random, randint, choice
from gamemath import Vector


class Card:
    def __init__(self):
        self.size = Vector(90, 120)
        self.srf = pg.Surface(self.size.tuple)

    def draw(self, game):
        game.after_render.append(lambda: game.srf.blit(self.srf, (game.dis.res.x - self.size.x, 0)))


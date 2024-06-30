import pygame as pg
from random import random, randint, choice
from gamemath import Vector
from planet_img_gen import gen_planet


class Card:
    def __init__(self):
        w = 150
        self.size = Vector(w, w*16//9)
        self.srf = pg.Surface(self.size.tuple)
        self.image = gen_planet(Vector([self.size.x*0.9]*2))
        self.srf.blit(self.image, (0,0))

    def draw(self, game):
        game.after_render.append(lambda: game.srf.blit(self.srf, (game.dis.res.x - self.size.x, 0)))


import pygame as pg
from random import random, randint, choice
from gamemath import Vector
from planet_img_gen import gen_planet

def percent(n: float):
    return f'{round(n*100)}%'

class Card:
    def __init__(self, star):
        self.star = star

        self.name = "Earth"
        self.wet = random()
        self.temp = random()

        w = 150
        self.size = Vector(w, w*16//9)
        self.srf = pg.Surface(self.size.tuple)

        self.image = gen_planet(Vector([self.size.x]*2), star, self.wet, self.temp)
        self.srf.blit(self.image, (0,0))

        self.text = f'NAME:{self.name}\nWET:{percent(self.wet)}\nTEMP:{percent(self.temp)}'
        print(self.text)

    def draw(self, game):
        game.after_render.append(lambda: game.srf.blit(self.srf, (game.dis.res.x - self.size.x, 0)))


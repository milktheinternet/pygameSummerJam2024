import pygame as pg
from random import random, randint, choice
from gamemath import Vector
from planet_img_gen import gen_planet
from planet_namer import name_planet
import math

font = pg.font.Font("assets/font.ttf", 12)

def percent(n: float):
    return f'{round(n*100)}%'

class Card:
    def __init__(self, game, star, bg=(20,20,20)):
        self.star = star
        self.bg = bg

        self.margin = 3
        self.wet = random()
        self.temp = random()
        self.wet = self.wet ** 1.1
        self.wet = self.wet * 0.5 + self.wet * math.sin(self.temp*math.pi) * 0.5

        self.name = name_planet(self.wet, self.temp)

        w = 150
        self.size = Vector(w, w*16//9)
        self.srf = pg.Surface(self.size.tuple)
        self.srf.fill(self.bg)

        self.planet = gen_planet(game, Vector([self.size.x-self.margin*2]*2), star, self.wet, self.temp)
        self.srf.blit(self.planet, (self.margin, self.margin))

        self.text = f'NAME:{self.name}\nWET:{percent(self.wet)}\nTEMP:{percent(self.temp)}'
        self.render_text()

    def render_text(self):
        text_srfs = []
        for line in self.text.split('\n'):
            text_srfs.append(font.render(line, False, (255,255,255)))
        x, y = self.margin, self.size.x
        for srf in text_srfs:
            self.srf.blit(srf, (x,y))
            y += srf.get_height()

    def draw(self, game):
        game.after_render.append(lambda: game.srf.blit(self.srf, (game.dis.res.x - self.size.x, 0)))


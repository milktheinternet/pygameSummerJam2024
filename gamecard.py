import pygame as pg
from random import random
from gamemath import Vector
from planet_img_gen import gen_planet
from planet_namer import name_planet
import math
from gameloading import show_progress

font = pg.font.Font("assets/font.ttf", 12)

def percent(n: float):
    return f'{round(n*100)}%'

class Card:
    def __init__(self, game, star, bg=(0, 0, 0)):
        self.star = star
        self.bg = bg

        self.margin = 3
        self.wet = random()
        self.temp = random()
        medtemp = math.sin(self.temp*math.pi)
        medwet = math.sin(self.wet*math.pi)
        self.wet = self.wet ** 1.1
        self.wet = self.wet * 0.5 + self.wet * medtemp * 0.5

        maxpop = medtemp * medwet * 100
        self.pop = int(random() * maxpop)

        self.name = name_planet(self.wet, self.temp)

        self.size = Vector(150, 200)
        self.srf = pg.Surface(self.size.tuple)

        self.planet = gen_planet(Vector([star.diameter]*2), self.wet, self.temp)

        self.redraw()

        for i in range(10):
            show_progress(i/10, game.dis, "Scanning...")
            game.clock.tick(10)

    def redraw(self):
        self.srf.fill(self.bg)
        self.srf.blit(pg.transform.smoothscale(self.planet, [self.size.x-self.margin*2]*2), (self.margin, self.margin))
        self.text = f'NAME:{self.name}\nWET:{percent(self.wet)}\nTEMP:{percent(self.temp)}\nPOP:{self.pop}'
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


from gamemath import *
from gamecard import Card
import pygame as pg


class Star(Vector):
    def __init__(self):
        super().__init__()
        self.rendered_at = Vector()

        self.MODE_NORMAL, self.MODE_HOVER, self.MODE_SELECT, self.MODE_ACTIVE, self.MODE_ZOOM_IN, self.MODE_ZOOM_OUT = \
            'normal hover select active zoom-in zoom-out'.split()
        self.mode = self.MODE_NORMAL

        self.card = None

        self.zoom_anim_time = 0
        self.zoom_anim_duration = 1000

        self.diameter = 300
        self.zoom_diameter = self.diameter

    def random(self):
        self.x, self.y = (super().random() * tau).tuple
        return self

    def deselect(self):
        if self.mode in (self.MODE_ACTIVE, self.MODE_ZOOM_IN):
            self.mode = self.MODE_ZOOM_OUT
            self.zoom_anim_time = 1
        elif self.mode != self.MODE_ZOOM_OUT:
            self.mode = self.MODE_NORMAL

    def update(self, game):
        dv = game.mouse - self.rendered_at
        mouse_over = abs(dv.x) < 5 and abs(dv.y) < 5
        if self.mode == self.MODE_SELECT:
            if mouse_over and game.click_inst:
                for star in game.stars:
                    star.deselect()
                self.mode = self.MODE_ZOOM_IN
                self.zoom_anim_time = 1
                game.selected_star = self
                game.click_inst = False
        elif self.mode in (self.MODE_NORMAL, self.MODE_HOVER):
            if mouse_over:
                if game.click_inst:
                    for star in game.stars:
                        star.deselect()
                    self.mode = self.MODE_SELECT
                    game.click_inst = False
                else:
                    self.mode = self.MODE_HOVER
            else:
                self.mode = self.MODE_NORMAL

        if self.zoom_anim_time:
            p = min(self.zoom_anim_time / self.zoom_anim_duration, 1)
            if self.mode == self.MODE_ZOOM_IN:
                self.zoom_diameter = self.diameter * p
            elif self.mode == self.MODE_ZOOM_OUT:
                self.zoom_diameter = max(self.diameter * (1-p), 1)
            self.zoom_diameter = round(self.zoom_diameter)
            self.zoom_anim_time += game.delta
            if p >= 1:
                if self.mode == self.MODE_ZOOM_IN:
                    self.mode = self.MODE_ACTIVE
                else:
                    self.mode = self.MODE_NORMAL
                self.zoom_anim_time = 0

    def draw(self, game):
        cam, dis, srf = game.camera, game.dis, game.srf
        pos = to_screen(self + cam, dis)
        if not pos:
            return
        self.rendered_at = pos
        x, y = round(pos).tuple
        if not(0 <= x < dis.res.x and 0 <= y < dis.res.y) and self.mode != self.MODE_ACTIVE:return

        if self.mode == self.MODE_SELECT:
            if not self.card:
                def fun():self.card = Card(game, self)
                game.after_render.append(fun)
            else:
                self.card.draw(game)
            pg.draw.circle(srf, (255, 0, 0), (x, y), 2)
        elif self.mode == self.MODE_NORMAL:
            color = (255, 255, 0) if self.card else (255, 255, 255)
            srf.set_at((x, y), color)
        elif self.mode == self.MODE_HOVER:
            pg.draw.circle(srf, (255, 255, 255), (x, y), 5, 1)
            srf.set_at((x, y), (255, 0, 0))
        elif self.mode in (self.MODE_ACTIVE, self.MODE_ZOOM_IN, self.MODE_ZOOM_OUT):
            w, h = [self.zoom_diameter if self.mode!=self.MODE_ACTIVE else self.diameter]*2
            game.after_render.append(
                lambda: srf.blit(pg.transform.smoothscale(self.card.planet, (w, h)), (x - w//2, y - h//2)))
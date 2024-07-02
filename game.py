from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'TRUE'

import pygame as pg
pg.init()

from gamemath import *
from gamedisplay import Display
from gamestar import Star, init_stars
from gamemenu import Menu
from gameover import GameOver
from srf_effects import *

font = pg.font.Font("assets/font.ttf", 12)
ID = 0


def nextID():
    global ID
    ID += 1
    return ID


def screenshot(srf: pg.Surface):
    pg.image.save(srf, f"assets/screenshots/image{nextID()}.png")


class Game:
    def __init__(self, dis:Display, menu: Menu = None, nstars=1000):

        init_stars()

        self.menu = menu

        self.font = font

        self.dis = dis
        self.srf = self.dis.srf

        self.active = True

        self.click_inst = False
        self.rclick_inst = False

        self.stars = []

        for i in range(nstars):
            star = Star(self)
            star.random()
            self.stars.append(star)

        self.after_render = []

        self.camera = Vector()

        self.up = self.down = self.left = self.right = False

        self.clock = pg.time.Clock()
        self.delta = 0.0001
        self.mouse = Vector(-100, -100)

        self.pop = 0
        self.max_pop = 10

        self.time = 1
        self.max_time = 1000 * 60 * 5 # aka 5 minutes

        self.fade_srf = pg.Surface(self.dis.res.tuple)
        self.fade_duration = 3 * 1000

        self.fail_abduct_srf = pg.Surface(self.dis.res.tuple)
        self.fail_abduct_srf.fill((255, 0, 0))
        self.fail_abduct_at = 0
        self.fail_abduct_dur = 500

        self.shake_for = 0
        self.shake_intensity = 0.01
        self.shake = Vector()

        self.supernova_at = 0
        self.supernova_dur = 30 * 1000
        self.supernova_srf = pg.Surface(self.dis.res.tuple)
        self.supernova_srf.fill((255, 255, 255))

        self.end_delay = 4000
        self.end_dur = 2000

        self.gameover_delay = 1000

        self.after_supernova = False
        self.survivor = None

        self.scan_effect = 0
        self.scan_height_range = (5, 10)

    def count_abandoned(self):
        return sum([star.card.pop for star in self.stars if star.card and not star.shield])

    @property
    def time_left(self):
        if self.supernova_at:
            s = "ZERO DAY"
        elif self.after_supernova:
            secs_since = (self.time-(self.max_time + self.supernova_dur))//1000
            mins_since = int(secs_since // 60)
            s = "TIME SINCE: "
            if mins_since:
                s = str(mins_since)+"m "
            s += str(int(secs_since % 60))+"s"
        else:
            secs_left = (self.max_time-self.time)//1000
            mins_left = int(secs_left // 60)
            s = "TIME LEFT: "
            if mins_left:
                s = str(mins_left)+"m "
            s += str(int(secs_left % 60))+"s"
        return s

    def update(self):
        self.shake_for -= self.delta
        if self.shake_for > 0:
            self.shake = (Vector.random() - Vector.HALF()) * self.shake_intensity
        else:
            self.shake = Vector()

        self.click_inst = False
        self.rclick_inst = False
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.up = True
                if event.key == pg.K_s:
                    self.down = True
                if event.key == pg.K_a:
                    self.left = True
                if event.key == pg.K_d:
                    self.right = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    self.up = False
                if event.key == pg.K_s:
                    self.down = False
                if event.key == pg.K_a:
                    self.left = False
                if event.key == pg.K_d:
                    self.right = False
                if event.key == pg.K_SPACE:
                    for star in self.stars:
                        star.deselect()
                if event.key == pg.K_x:
                    screenshot(self.srf)
                if event.key in (pg.K_ESCAPE, pg.K_p):
                    def on_quit():
                        self.active = False

                    menu = Menu({
                        "CONTINUE": None,
                        "ABANDON THE UNIVERSE": on_quit
                    }, self.dis)
                    menu.make_btns()
                    menu.start()
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click_inst = True
                if event.button == 3:
                    self.rclick_inst = True
            elif event.type == pg.QUIT:
                self.active = False
        self.mouse = (Vector(pg.mouse.get_pos()) - self.dis.srfpos) / self.dis.scaled_res * self.dis.res

        speed = 0.001 * self.delta
        if (self.left or self.right) and (self.up or self.down):
            speed *= 0.7
        if self.up:
            self.camera.y += speed
        if self.down:
            self.camera.y -= speed
        if self.left:
            self.camera.x += speed
        if self.right:
            self.camera.x -= speed

        for star in self.stars:
            star.update(self)

            if star.mode == star.MODE_ZOOM_IN or (star.mode == star.MODE_ACTIVE and self.after_supernova):
                star.x, star.y = trim_angle_vec(star).tuple
                self.camera = trim_angle_vec(self.camera)
                self.camera -= (self.camera + star)/20

        if self.time > self.max_time and not self.supernova_at and not self.after_supernova:
            self.start_supernova()

        self.time += self.delta

    def draw_compass(self, pos = None, radius = 20):
        cx, cy, cz = angle_to_3d(self.camera)
        compass = Vector(cx, cy)
        center = pos if pos else self.dis.res*0.5

        def a(): pg.draw.circle(self.srf, (255, 0, 0), (compass * radius + center).tuple, 3)
        def c(): pg.draw.line(self.srf, (255, 255, 255), (compass * radius + center).tuple, (compass * -radius + center).tuple, 1)
        def b(): pg.draw.circle(self.srf, (0, 0, 255), (compass * -radius + center).tuple, 3)
        if cz > 0:
            (a(), c(), b())
        else:
            (b(), c(), a())

        pg.draw.circle(self.srf, (255, 255, 255), center.tuple, 20, 1) # compass outline

    def draw_stats(self):
        stats_str = f"ABDUCTED: {self.pop}/{self.max_pop}\n{self.time_left}"
        y = self.dis.res.y
        for line in stats_str.split('\n'):
            srf = font.render(line, False, (255, 255, 255))
            y -= srf.get_height()
            self.srf.blit(srf, (0, y))

    def draw_stars(self):
        for star in self.stars:
            star.draw()

    def start_supernova(self):
        self.supernova_at = self.time
        self.scan_height_range = (1,5)
        self.shake_for = self.supernova_dur+500
        for star in self.stars:
            star.start_supernova()

    def end_supernova(self):
        self.scan_effect = 0
        self.supernova_at = 0
        self.after_supernova = True

    def end_game(self):
        self.active = False
        end_pop = self.survivor.card.pop if self.survivor else 0
        abandoned = self.count_abandoned()
        visited = sum([1 for star in self.stars if star.card])
        GameOver(self.dis, end_pop, abandoned, visited).start()

    def screen_effects(self):
        if self.fail_abduct_at:
            p = (self.time-self.fail_abduct_at)/self.fail_abduct_dur
            if p > 1:
                self.fail_abduct_at = 0
            self.fail_abduct_srf.set_alpha(round((1-p) * 255))
            self.srf.blit(self.fail_abduct_srf, (0, 0))

        if self.time < self.fade_duration:
            p = self.time/self.fade_duration
            self.fade_srf.set_alpha(round((1-p) * 255))
            self.srf.blit(self.fade_srf, (0, 0))

        if self.supernova_at:
            p = (self.time-self.supernova_at)/self.supernova_dur
            self.scan_effect = int(p**2*20)
            if p > 1:
                self.end_supernova()
            self.shake_intensity = 0.04 * p ** 2
            self.supernova_srf.set_alpha(round(p * 255))
            self.srf.blit(self.supernova_srf, (0, 0))
        elif self.after_supernova:
            time_since = self.time - self.max_time - self.supernova_dur
            if time_since > self.end_delay + self.end_dur + self.gameover_delay:
                self.end_game()
            if time_since > self.end_delay:
                p = (time_since - self.end_delay)/self.end_dur
                p = min(1, p)
                yp = p*self.dis.res.y//2+1
                pg.draw.rect(self.srf, (0, 0, 0), (0, 0, self.dis.res.x, yp))
                pg.draw.rect(self.srf, (0, 0, 0), (0, self.dis.res.y-yp, self.dis.res.x, yp))

        if self.scan_effect:
            scanlines(self.srf, self.scan_height_range, (-self.scan_effect, self.scan_effect))

    def render(self):
        self.srf.fill((30, 20, 40))

        self.draw_stars()

        for fun in self.after_render:
            fun()
        self.after_render = []

        self.draw_compass(Vector(20,20))
        self.draw_stats()

        self.screen_effects()

        self.dis.update()
        self.clock.tick(60)
        self.delta = self.clock.get_time()

    def start(self):
        self.active = True
        while self.active:
            self.update()
            self.render()
        if self.menu:
            self.menu.start()

if __name__ == "__main__":
    res = Vector(480, 360)
    winres = res * 2
    dis = Display(res, winres)
    game = Game(dis)
    game.start()
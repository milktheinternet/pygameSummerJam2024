from gamemath import *
from gamecard import Card
import pygame as pg
from random import randint

STAR_RES = Vector(9, 9)
STAR_IMG = pg.image.load("assets/beauty/stars.png")
DISCOVERED_IMG = pg.image.load("assets/beauty/stars_known.png")
NSTARS = STAR_IMG.get_height()//STAR_RES.y
STARS = []
DISCOVERED = []


def init_stars():
    global STARS, STAR_IMG, DISCOVERED_IMG
    STAR_IMG = STAR_IMG.convert_alpha()
    DISCOVERED_IMG = DISCOVERED_IMG.convert_alpha()
    for y in range(0, NSTARS):
        rect = (0, y*STAR_RES.y, STAR_RES.x, STAR_RES.y)
        STARS.append(STAR_IMG.subsurface(rect))
        DISCOVERED.append(DISCOVERED_IMG.subsurface(rect))


class Star(Vector):
    def __init__(self, game):
        super().__init__()

        self.twinkle_offset = randint(0, 10000)
        self.twinkle_dur = 1000

        self.game = game

        self.rendered_at = Vector()

        self.MODE_NORMAL, self.MODE_HOVER, self.MODE_SELECT, self.MODE_ACTIVE, self.MODE_ZOOM_IN, self.MODE_ZOOM_OUT,\
            self.MODE_SUPERNOVA = range(7)
        self.mode = self.MODE_NORMAL

        self.card = None

        self.zoom_anim_time = 0
        self.zoom_anim_duration = 1000

        self.diameter = 300
        self.zoom_diameter = self.diameter

        self.people = []

        self.shield = None
        self.shield_at = 0
        self.shield_layers = 0
        self.shield_diameter = int(self.diameter * 1.1)
        self.shield_fade_dur = 1000
        self.shield_flash_dur = 300

    def start_supernova(self):
        if self.mode == self.MODE_ACTIVE or self.mode == self.MODE_ZOOM_IN:
            self.make_shield()
            self.game.survivor = self
        else:
            self.supernova_at = 0
            self.supernova_delay = 3000 * random()
            self.supernova_fade_dur = 3000
            self.supernova_dur = self.game.supernova_dur - self.supernova_delay - self.supernova_fade_dur

            self.mode = self.MODE_SUPERNOVA
            self.supernova_at = self.game.time

    def make_shield(self):
        self.shield_at = self.game.time
        self.shield = pg.Surface([self.shield_diameter]*2, pg.SRCALPHA)
        shield_rad = self.shield_diameter//2
        for i in range(shield_rad, 0, -1):
            pg.draw.circle(self.shield, (0, 255, 255, int(i/shield_rad*255)), (shield_rad, shield_rad), i)

    @property
    def radius(self):
        return self.diameter/2

    def random(self):
        self.x, self.y = ((super().random()-Vector.HALF()) * tau).tuple
        return self

    def deselect(self):
        if self.mode in (self.MODE_SUPERNOVA, self.MODE_ZOOM_OUT) or self.game.supernova_at:
            return
        if self.mode in (self.MODE_ACTIVE, self.MODE_ZOOM_IN):
            self.mode = self.MODE_ZOOM_OUT
            self.zoom_anim_time = 1
        else:
            self.mode = self.MODE_NORMAL

    def initiate(self, game):
        self.card = Card(game, self)
        self.people = [Person(self) for _ in range(self.card.pop)]

    def reverse_abduct(self):
        if self.game.pop > 0:
            self.game.pop -= 1
            self.card.pop += 1
            self.card.redraw()
            self.people.append(Person(self, tracked=True))

    def update(self, game):
        dv: Vector = game.mouse - self.rendered_at
        mouse_over = abs(dv.x) < 5 and abs(dv.y) < 5
        if self.mode == self.MODE_ACTIVE:
            for person in self.people:
                person.update()
            if dv.dist < self.diameter/2:
                if game.click_inst:
                    game.click_inst = False
                    self.reverse_abduct()
        elif self.mode == self.MODE_SELECT:
            if mouse_over and game.click_inst:
                game.stars.remove(self)
                for star in game.stars:
                    if isinstance(star, Star):
                        star.deselect()
                game.stars.insert(0, self)
                self.mode = self.MODE_ZOOM_IN
                self.zoom_anim_time = 1
                game.selected_star = self
                game.click_inst = False
        elif self.mode in (self.MODE_NORMAL, self.MODE_HOVER):
            if mouse_over:
                if game.click_inst:
                    for star in game.stars:
                        if isinstance(star, Star):
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
                self.zoom_diameter = self.diameter * p ** 2
            elif self.mode == self.MODE_ZOOM_OUT:
                self.zoom_diameter = max(self.diameter * (1 - p**2), 1)
            self.zoom_diameter = round(self.zoom_diameter)
            self.zoom_anim_time += game.delta
            if p >= 1:
                if self.mode == self.MODE_ZOOM_IN:
                    self.mode = self.MODE_ACTIVE
                else:
                    self.mode = self.MODE_NORMAL
                self.zoom_anim_time = 0

    def draw_shield(self, x, y):
        if self.shield:
            w = h = self.shield_diameter
            time_since = self.game.time - self.shield_at
            if time_since < self.shield_fade_dur:
                p = time_since/self.shield_fade_dur
                self.shield.set_alpha(int(p*255))
            else:
                time_since -= self.shield_fade_dur
                p = time_since/self.shield_fade_dur
                p = sin(p*pi)
                self.shield.set_alpha(155+int(p*100))
            self.game.srf.blit(self.shield, (x - w // 2, y - h // 2))

    def draw_planet(self, x, y):
        w, h = [self.zoom_diameter if self.mode != self.MODE_ACTIVE else self.diameter] * 2
        self.game.srf.blit(pg.transform.smoothscale(self.card.planet, (w, h)), (x - w // 2, y - h // 2))
        if self.mode == self.MODE_ACTIVE:
            for person in self.people:
                person.draw(self.game.dis)
            self.draw_shield(x, y)

            # display number of people on the planet
            srf = self.game.font.render(str(self.card.pop), True, (255, 255, 255))
            size = [2*n for n in srf.get_size()]
            self.game.srf.blit(pg.transform.scale(srf, size), (x - size[0]//2, y - size[1] - self.radius))

    def draw_star(self, x, y):
        x, y = round(Vector(x, y) - STAR_RES/2).tuple
        p = ((self.twinkle_offset + self.game.time)/self.twinkle_dur)%1
        img = (DISCOVERED if self.card else STARS)[int(p*NSTARS)]
        self.game.srf.blit(img, (x,y))

    def draw_supernova(self, x, y):
        game = self.game
        p = (game.time-(self.supernova_at + self.supernova_delay))/self.supernova_dur
        radius = p * 100 * (0.8 + (random()-0.5)*(0.2 * 2))
        if p > 1:
            p = 1 - (game.time - self.supernova_at - self.supernova_dur)/self.supernova_fade_dur
            if p < 0:
                return
            v = min(255, max(0, int((p) * 255)))
            if -radius <= x < game.dis.res.x + radius and -radius <= y < game.dis.res.y + radius:
                pg.draw.circle(game.srf, (v, v, v), (x, y), radius)
        elif p > 0:
            if -radius <= x < game.dis.res.x + radius and -radius <= y < game.dis.res.y + radius:
                pg.draw.circle(game.srf, (255, 255, 255), (x, y), radius)
                if radius < 5: self.draw_star(x, y)
        else:
            self.draw_star(x, y)

    def draw(self):
        game = self.game
        cam, dis, srf = game.camera, game.dis, game.srf
        pos = to_screen(self + cam + game.shake, dis)
        if not pos:
            return
        self.rendered_at = pos
        x, y = round(pos).tuple
        if not(0 <= x < dis.res.x and 0 <= y < dis.res.y) and self.mode not in (self.MODE_ACTIVE, self.MODE_SUPERNOVA):
            return

        if self.mode == self.MODE_SELECT:
            if not self.card:
                def fun():
                    self.initiate(game)
                game.after_render.append(fun)
            else:
                self.card.draw(game)
            pg.draw.circle(srf, (255, 0, 0), (x, y), 5)
        elif self.mode == self.MODE_NORMAL:
            self.draw_star(x, y)
        elif self.mode == self.MODE_HOVER:
            self.draw_star(x, y)
            pg.draw.circle(srf, (255, 255, 255), (x, y), 5, 1)
        elif self.mode in (self.MODE_ACTIVE, self.MODE_ZOOM_IN, self.MODE_ZOOM_OUT):
            game.after_render.append(lambda:self.draw_planet(x, y))
        elif self.mode == self.MODE_SUPERNOVA:
            self.draw_supernova(x, y)


class Person(Vector):
    def __init__(self, star: Star, tracked: bool = False):
        self.game = star.game
        self.star = star
        ONE = Vector(1, 1)
        super().__init__(self.random()*2 - ONE)

        while self.dist > 1:
            self.set(self.random()*2 - ONE)

        self.set(self * star.radius)

        self.speed = 1/150  # up to 1 pixel every 150 ms
        self.hover = False
        self.tracked = tracked

        self.abducted = 0
        self.abduct_anim_dur = 100

    def abduct(self, game):
        if game.pop < game.max_pop:
            game.pop += 1
            self.star.card.pop -= 1
            self.star.card.redraw()
            self.abducted = game.time
        else:
            game.fail_abduct_at = game.time

    def update(self):

        game = self.game

        if self.abducted:
            if game.time - self.abducted > self.abduct_anim_dur:
                self.star.people.remove(self)
            return

        self.hover = (game.mouse - self.true_pos).dist < 10
        if self.hover and game.rclick_inst:
            self.abduct(game)

        def moved():
            return self + (self.random()*2 - Vector(1, 1)) * game.delta * self.speed
        goal = moved()
        i = 0
        while goal.dist > self.star.radius:
            if i > 100:
                self.__init__(self.star)
                goal = self
                break
            else:
                goal = moved()
            i += 1

        self.set(goal)

    @property
    def true_pos(self):
        return round(self + self.star.rendered_at)

    def draw(self, dis):
        x, y = self.true_pos.tuple
        if 0 <= x < dis.res.x and 0 <= y < dis.res.y:
            if self.abducted:
                p = (self.game.time - self.abducted)/self.abduct_anim_dur
                pg.draw.circle(dis.srf, (255, 255, 255), (x, y), int(p*10))
            else:
                if self.hover:
                    pg.draw.circle(dis.srf, (255, 255, 255), (x, y), 10, 1)
            dis.srf.set_at((x, y), (0, 255, 0) if self.tracked else (0, 0, 0))

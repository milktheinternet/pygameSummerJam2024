import pygame as pg
__import__('os').environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'TRUE'
pg.init()

from gamemath import *
from gamedisplay import Display
from gamestar import Star
#import gamemusic

class Game:
    def __init__(self, nstars=1000, winres=Vector(500*16//9, 500), res=Vector(480, 360)):
        self.dis = Display(res, winres)
        self.srf = self.dis.srf
        self.active = True

        self.click_inst = False

        self.stars = []

        for i in range(nstars):
            star = Star()
            star.random()
            self.stars.append(star)
        self.after_render = []

        self.camera = Vector()

        self.up = self.down = self.left = self.right = False

        self.clock = pg.time.Clock()
        self.delta = 0.0001
        self.mouse = Vector(-100, -100)

    def update(self):

        self.click_inst = False
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
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.click_inst = True
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

    def draw_stars(self):
        for star in self.stars:
            star.draw(self)

    def render(self):
        self.srf.fill((30, 20, 40))

        self.draw_stars()

        self.draw_compass(Vector(20,20))

        for fun in self.after_render:
            fun()
        self.after_render = []

        self.dis.update()
        self.clock.tick(60)
        self.delta = self.clock.get_time()

    def start(self):
        self.active = True
        while self.active:
            self.update()
            self.render()

if __name__ == "__main__":
    demo = Game(winres=Vector(480*2, 360*2))
    demo.start()
    pg.display.quit()
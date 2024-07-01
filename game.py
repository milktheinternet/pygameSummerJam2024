import pygame as pg
__import__('os').environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'TRUE'
pg.init()

from gamemath import *
from gamedisplay import Display
from gamestar import Star
import gamemusic

font = pg.font.Font("assets/font.ttf", 12)
font_big = pg.font.Font("assets/font.ttf", 24)

class Game:
    def __init__(self, nstars=1000, winres=Vector(500*16//9, 500), res=Vector(480, 360)):
        self.dis = Display(res, winres)
        self.srf = self.dis.srf
        self.active = True

        self.click_inst = False
        self.rclick_inst = False

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

        self.pop = 0
        self.max_pop = 10

        self.time = 0
        self.max_time = 1000 * 60 * 10

    @property
    def time_left(self):
        return str(int((self.max_time-self.time)//1000//60 % 60))+"m "+str(int((self.max_time-self.time)//1000 % 60))+"s"

    def update(self):

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

            if star.mode in (star.MODE_ZOOM_IN,):
                star.x, star.y = trim_angle_vec(star).tuple
                self.camera = trim_angle_vec(self.camera)
                self.camera -= (self.camera + star)/20

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
        stats_str = f"ABDUCTED: {self.pop}/{self.max_pop}\nTIME LEFT: {self.time_left}"
        y = self.dis.res.y
        for line in stats_str.split('\n'):
            srf = font.render(line, False, (255, 255, 255))
            y -= srf.get_height()
            self.srf.blit(srf, (0, y))

    def draw_stars(self):
        for star in self.stars:
            star.draw(self)

    def render(self):
        self.srf.fill((30, 20, 40))

        self.draw_stars()

        for fun in self.after_render:
            fun()
        self.after_render = []

        self.draw_compass(Vector(20,20))
        self.draw_stats()

        self.dis.update()
        self.clock.tick(60)
        self.delta = self.clock.get_time()

    def start(self):
        self.active = True
        while self.active:
            self.update()
            self.render()

if __name__ == "__main__":
    gamemusic.play()
    demo = Game(winres=Vector(480*2, 360*2))
    demo.start()
    pg.display.quit()
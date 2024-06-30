import pygame as pg
from gamemath import *
from gamedisplay import Display
from gamecard import Card

__import__('os').environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'TRUE'
pg.init()


class Star(Vector):
    def __init__(self):
        super().__init__()
        self.rendered_at = Vector()

        self.MODE_NORMAL, self.MODE_HOVER, self.MODE_SELECT, self.MODE_ACTIVE = 'normal hover select active'.split()
        self.mode = self.MODE_NORMAL

        self.card = None

    def random(self):
        self.x, self.y = (super().random() * tau).tuple
        return self

    def update(self, game):
        dv = game.mouse - self.rendered_at
        if self.mode in (self.MODE_NORMAL, self.MODE_HOVER):
            if abs(dv.x) < 5 and abs(dv.y) < 5:
                if game.click_inst:
                    self.mode = self.MODE_SELECT
                    game.selected_star = self
                else:
                    self.mode = self.MODE_HOVER
            else:
                self.mode = self.MODE_NORMAL

    def draw(self, game):
        cam, dis, srf = game.camera, game.dis, game.srf
        pos = to_screen(self + cam, dis)
        if not pos:
            return
        self.rendered_at = pos
        x, y = round(pos).tuple
        if 0 <= x < dis.res.x and 0 <= y < dis.res.y:
            if self.mode == self.MODE_SELECT:
                if not self.card:
                    self.card = Card(self)
                self.card.draw(game)
                color = (255, 0, 0)
                pg.draw.circle(srf, color, (x, y), 1)
            else:
                color = (255, 255, 255)
                if self.mode == self.MODE_HOVER:
                    color = (255, 0, 0)
                    pg.draw.circle(srf, (255, 255, 255), (x, y), 5, 1)
                srf.set_at((x, y), color)


class Game:
    def __init__(self, nstars=1000, winres=Vector(500*16//9, 500), res=Vector(480, 360)):
        self.dis = Display(res, winres)
        self.srf = self.dis.srf
        self.active = True

        self.stars = []

        for i in range(nstars):
            star = Star()
            star.random()
            self.stars.append(star)

        self.selected_star = self.stars[-1]
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
                self.selected_star.mode = self.selected_star.MODE_NORMAL
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
    demo = Game()
    demo.start()
    pg.display.quit()
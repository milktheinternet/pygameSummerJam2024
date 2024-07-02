import pygame as pg
from gamemath import Vector
from gamemenu import Button
from os import listdir

# slideshow paths must end in '/'
TUT_PATH = "assets/slideshows/XX/"


class Slideshow:
    def __init__(self, dis, menu, name='tutorial'):
        path = TUT_PATH.replace('XX', name)

        self.font = pg.font.Font("assets/font.ttf", 12)
        self.menu = menu
        self.mouse = (0,0)
        self.click = False
        self.dis = dis
        self.active = True
        self.buttons = []

        self.slide = 0
        self.slideshow = [pg.image.load(path + file).convert()
                          for file in sorted(listdir(path))
                          if file[-4:]=='.png']
        self.slideshow = [pg.transform.smoothscale(img, self.dis.res.tuple) for img in self.slideshow]

        self.make_btns()

    def next(self):
        self.slide = (self.slide + 1)%len(self.slideshow)
        self.make_btns()
        self.start()

    def prev(self):
        self.slide = (self.slide - 1)%len(self.slideshow)
        self.make_btns()
        self.start()

    def make_btns(self):
        self.buttons = []
        for x, y, w, h, text, on_click in ((0, 0, 30, 14, "BACK", None),
                                           (35, 0, 30, 14, "PREV", self.prev),
                                           (70, 0, 30, 14, "NEXT", self.next),
                                           (105, 0, 30, 14, f"{self.slide+1}/{len(self.slideshow)}", None)):
            self.buttons.append(Button(self, text, on_click, (x, y), (w, h)))

    def start(self):
        while self.active:
            self.update()
            self.render()
        self.menu.start()

    def close(self):
        self.active = False

    def update(self):
        self.click = False
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                self.click = True
            elif event.type == pg.QUIT:
                self.active = False
        self.mouse = round((Vector(pg.mouse.get_pos())-self.dis.srfpos)/self.dis.scaled_res*self.dis.res).tuple

        for button in self.buttons:
            button.update()

    def render(self):
        self.dis.srf.blit(self.slideshow[self.slide],(0,0))
        for button in self.buttons:
            button.render()
        self.dis.update()
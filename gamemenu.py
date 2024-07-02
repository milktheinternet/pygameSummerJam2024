import pygame as pg
from gamemath import Vector

EXAMPLE_OPTIONS = {
    "PLAY": lambda: None,
    "SETTINGS": lambda: None,
    "TUTORIAL!": lambda: None
}


class Button:
    def __init__(self, menu, text, on_click, pos, size, hoverbg=(50,50,50), bg=(0,0,0)):
        self.bg, self.hoverbg = bg, hoverbg

        self.menu = menu
        self.pos = pos
        self.size = size
        self.text = text
        self.on_click = on_click

        self.srf = pg.Surface(size)
        srf = menu.font.render(self.text, False, (255,255,255))
        self.text_srf = srf

    def draw_text_srf(self):
        w, h = self.text_srf.get_size()
        x = (self.size[0]-w)//2
        y = (self.size[1]-h)//2
        self.srf.blit(self.text_srf, (x, y))

    def update(self):
        mx, my = self.menu.mouse
        x, y = self.pos
        w, h = self.size
        if x <= mx < x + w and y <= my < y + h:
            self.srf.fill(self.hoverbg)
            if self.menu.click:
                if self.on_click:
                    self.on_click()
                self.menu.close()
        else:
            self.srf.fill(self.bg)
        self.draw_text_srf()

    def render(self):
        self.menu.dis.srf.blit(self.srf, self.pos)

class Menu:
    def __init__(self, options: dict, dis):
        self.font = pg.font.Font("assets/font.ttf", 12)
        self.options = options
        self.mouse = (0,0)
        self.click = False
        self.dis = dis
        self.active = True
        self.buttons = []

    def make_btns(self):
        options, dis = self.options, self.dis
        self.buttons = []
        x,y = 0, 0
        w,h = dis.res.x, dis.res.y//len(options)
        for text, on_click in options.items():
            self.buttons.append(Button(self, text, on_click, (x, y), (w,h),
                                       bg=(50, 0, 0) if text[-1] == '!' else (0, 0, 0)))
            y += h

    def start(self):
        while self.active:
            self.update()
            self.render()

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
        self.dis.srf.fill((0,0,0))
        for button in self.buttons:
            button.render()
        self.dis.update()
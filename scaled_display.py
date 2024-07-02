import pygame as pg
from gamemath import Vector

class Display:
    def __init__(self, res: Vector, winres: Vector):
        self.bg = (0, 0, 0)
        self.winsrf = pg.display.set_mode(winres.tuple if winres else (0,0), pg.FULLSCREEN if winres==(0,0) else 0)
        winres = Vector(self.winsrf.get_size())
        self.srf = pg.Surface(res.tuple)

        w, h = res.tuple
        ww, wh = winres.tuple
        if ww/w*h > wh:
            sh = wh
            sw = wh/h*w
        else:
            sw = ww
            sh = ww/w*h

        self.scaled_res = Vector(sw, sh)

        self.res, self.winres = res, winres
        self.srfpos = round((winres-self.scaled_res)/2)

    def update(self):
        self.winsrf.fill(self.bg)
        self.winsrf.blit(pg.transform.scale(self.srf, self.scaled_res.tuple), self.srfpos.tuple)
        pg.display.update()
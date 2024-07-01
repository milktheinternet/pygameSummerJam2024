import pygame as pg
from gamemath import Vector

font = pg.font.Font("assets/font.ttf", 12)

def show_progress(p, dis, msg="Loading..."):
    bg = (0,0,0)
    bar_color = (0, 255, 255)
    size = round(dis.res/2)
    pos: Vector = dis.res/4
    pg.draw.rect(dis.srf, bg, (pos.x, pos.y, size.x, size.y))
    bar_size = Vector(0.9*p, 0.1) * size
    margin = size.x*0.05
    bar_pos = pos + Vector(margin, (size.y - bar_size.y)/2)
    pg.draw.rect(dis.srf, bar_color, (bar_pos.x, bar_pos.y, bar_size.x, bar_size.y))

    msgsrf = font.render(msg, False, (255,255,255), (0,0,0))
    dis.srf.blit(msgsrf, (bar_pos.x, bar_pos.y - msgsrf.get_height()))

    dis.update()
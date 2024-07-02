from game import Game
from menus import Menu
from scaled_display import Display
from gamemath import Vector
from gameover import set_highscore

from slides import Slideshow

import music
# 430-930 sat sun

has_seen_tutorial = 'YES' in open('assets/has_seen_tutorial', 'r').read()

def newgame(menu):
    Game(dis, menu).start()

def tutorial(menu):
    open("assets/has_seen_tutorial",'w').write('YES')
    Slideshow(dis, menu, 'tutorial').start()

def credits(menu):
    Slideshow(dis, menu, 'credits').start()

def change_music(menu):
    music.MusicSettings(dis, menu).start()

if __name__ == "__main__":
    res = Vector(480, 360)
    winres = None#res * 2
    dis = Display(res, winres)

    menu = Menu({
        "PLAY": lambda: newgame(menu),
        "TUTORIAL"+("" if has_seen_tutorial else "!"): lambda: tutorial(menu),
        "CREDITS": lambda: credits(menu),
        "CHANGE MUSIC": lambda: change_music(menu),
        "QUIT": None}, dis)

    menu.options["RESET HIGHSCORE"] = lambda: (
        open("assets/has_seen_tutorial",'w').write('NO'),
        set_highscore(0),
        menu.start())

    music_on, music_off = "MUSIC: ON", "MUSIC: OFF"
    def music_on_fun():
        if music_off in menu.options.keys():del menu.options[music_off]
        menu.options[music_on] = music_off_fun
        menu.make_btns()
        music.play()
        menu.start()

    def music_off_fun():
        if music_on in menu.options.keys():del menu.options[music_on]
        menu.options[music_off] = music_on_fun
        menu.make_btns()
        music.pause()
        menu.start()

    music_on_fun()
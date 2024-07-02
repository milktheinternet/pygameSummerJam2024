from game import Game
from gamemenu import Menu
from gamedisplay import Display
from gamemath import Vector
from gameover import set_highscore

from tutorial import Tutorial

import gamemusic
# 430-930 sat sun

has_seen_tutorial = 'YES' in open('assets/has_seen_tutorial', 'r').read()

def newgame(menu):
    Game(dis, menu).start()

def tutorial(menu):
    open("assets/has_seen_tutorial",'w').write('YES')
    Tutorial(dis, menu).start()

if __name__ == "__main__":
    res = Vector(480, 360)
    winres = None#res * 2
    dis = Display(res, winres)

    menu = Menu({
        "PLAY": lambda: newgame(menu),
        "TUTORIAL"+("" if has_seen_tutorial else "!"): lambda: tutorial(menu),
        "QUIT": None}, dis)

    menu.options["RESET HIGHSCORE"] = lambda: (set_highscore(0), menu.start())

    music_on, music_off = "MUSIC: ON", "MUSIC: OFF"
    def music_on_fun():
        if music_off in menu.options.keys():del menu.options[music_off]
        menu.options[music_on] = music_off_fun
        menu.make_btns()
        gamemusic.play()
        menu.start()

    def music_off_fun():
        if music_on in menu.options.keys():del menu.options[music_on]
        menu.options[music_off] = music_on_fun
        menu.make_btns()
        gamemusic.pause()
        menu.start()

    music_on_fun()
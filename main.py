from game import Game
from gamemenu import Menu
from gamedisplay import Display
from gamemath import Vector
import gamemusic
# 430-930 sat sun


def newgame():
    game = Game(dis)
    game.start()

if __name__ == "__main__":
    res = Vector(480, 360)
    winres = None#res * 2
    dis = Display(res, winres)

    menu = Menu({
        "PLAY": newgame,
        "TUTORIAL": None,
        "QUIT": None}, dis)
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

    music_off_fun()
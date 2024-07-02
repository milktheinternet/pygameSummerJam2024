from pygame import mixer_music as mixer
from os import listdir
from menus import Menu

MUSIC_DIR = "assets/music/"


def list_tracks():
    return [file[:-4] for file in listdir(MUSIC_DIR)]


def switch_song(song):
    mixer.unload()
    mixer.load(MUSIC_DIR + song + '.mp3')
    mixer.play(1000)

switch_song("Vivaldi - The Four Sesons, Winter")
play = mixer.unpause
pause = mixer.pause


class MusicSettings(Menu):
    def __init__(self, dis, menu):

        self.menu = menu
        options = {
            "BACK":None,
        }
        def make_switch_func(song):
            return lambda: self.switch_song(song)
        for song in list_tracks():
            options[song] = make_switch_func(song)

        super().__init__(options, dis)
        self.make_btns()

    def switch_song(self, song):
        print("switching to ",song)
        switch_song(song)
        self.start()

    def close(self):
        super().close()
        self.menu.start()


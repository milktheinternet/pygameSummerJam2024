from pygame import mixer_music as mixer
mixer.load("assets/winter_vivaldi.mp3")
mixer.play(1_000_000_000)  # if you listen to this one billion times you're a pogchamp
play = mixer.unpause
pause = mixer.pause
pause()
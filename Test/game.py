import game_framework

from pico2d import *
import main
import title
open_canvas(800, 600, sync=True)
#open_canvas(800,600)
bgm = load_music('Squarium.mp3')
bgm.set_volume(25)
bgm.repeat_play()
game_framework.run(title)
close_canvas()

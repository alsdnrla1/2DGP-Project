import game_framework
from pico2d import *

import main
import title



name = "EndingState"
image = None
font = None

def enter():
    global image, bg, font
    image = load_image('ending.png')
    font = load_font('ENCR10B.TTF', 50)




def exit():
    global image
    del(image)



def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()

            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(title)



def draw(frame_time):
    clear_canvas()
    image.draw(400,300)
    font.draw(170, 250, 'You Died %d Times' % (main.deathcount), (255, 255, 255))
    update_canvas()







def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass







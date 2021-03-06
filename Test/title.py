import game_framework
from pico2d import *

import main



name = "TitleState"
image = None


def enter():
    global image, bg
    image = load_image('title.png')
    hide_cursor()


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
                game_framework.change_state(main)



def draw(frame_time):
    clear_canvas()
    image.draw(400,300)
    update_canvas()







def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass







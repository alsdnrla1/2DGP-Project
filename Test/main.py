import random

import game_framework
from pico2d import *



name = "MainState"

guy = None
bg = None
view = None

class Background:
    def __init__(self):
        self.x, self.y = 0,0
        self.image = load_image('technology1.jpg')
    def update(self,other):
        if other.position == other.BOTTOM:
            self.x -= 20
        elif other.position == other.TOP:
            self.x += 20
        elif other.position == other.RIGHT:
            self.y -= 20
        elif other.position == other.LEFT:
            self.y += 20

        if self.x == -1600 or self.x == 1600:
            self.x = 0
        if self.y == -1600 or self.y == 1600:
            self.y = 0

    def draw(self):
        self.image.draw(self.x, self.y)
        self.image.draw(self.x + 1600, self.y)
        self.image.draw(self.x - 1600, self.y)
        self.image.draw(self.x + 1600, self.y + 1600)
        self.image.draw(self.x - 1600, self.y + 1600)
        self.image.draw(self.x + 1600, self.y - 1600)
        self.image.draw(self.x - 1600, self.y - 1600)
        self.image.draw(self.x, self.y + 1600)
        self.image.draw(self.x, self.y - 1600)

class View:
    def __init__(self):
        self.x, self.y = 400,300

    def update(self, other):
        if other.position == other.BOTTOM:
            self.x = max(other.x, self.x)
        elif other.position == other.TOP:
            self.x = min(other.x, self.x)
        elif other.position == other.RIGHT:
            self.y = max(other.y, self.y)
        elif other.position == other.LEFT:
            self.y = min(other.y, self.y)


class Guy:
    jumping = None
    RUN, JUMP, SPIN = 0, 1, 2
    TOP, BOTTOM, LEFT, RIGHT = 6, 0, 9, 3
    action, position = RUN, BOTTOM
    def __init__(self):
        self.x, self.y = 100, 90
        self.frame = 0
        self.image = load_image('guy.png')
        self.dir = 1


    def update(self):
        if self.action == self.RUN:
            self.frame = (self.frame + 1) % 6
            self.x += 10

        elif self.action == self.JUMP:
            if self.jumping == None:
                self.jumping = True
                self.frame = 0
            else:
                if self.frame < 7:
                    self.x += 20 * self.dir
                    if self.frame < 2:
                        self.y += 70
                    elif self.frame > 4:
                        self.y -= 70
                    self.frame = (self.frame + 1) % 8
                else:
                    self.jumping = None
                    self.action = self.RUN
                    self.frame = 0
    def draw(self):
        self.image.clip_draw(self.frame * 100, (11 -self.action -self.position) * 100, 100, 100, self.x, self.y)


def enter():
    global guy, bg, view
    guy = Guy()
    bg = Background()
    view = View()


def exit():
    global guy, bg, view
    del(guy)
    del(bg)
    del(view)



def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            guy.action = guy.JUMP
        elif event.type == SDL_KEYDOWN and event.key == SDLK_c:
            guy.action = guy.SPIN
        #elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            #game_framework.push_state(pause_state)


def update():
    guy.update()
    #bg.update(view)
    view.update(guy)
    delay(0.05)


def draw():
    clear_canvas()
    bg.draw()
    guy.draw()
    update_canvas()





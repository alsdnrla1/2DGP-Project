import random

import game_framework
from pico2d import *

from guy import Guy
from wall import Wall
from background import Background
name = "MainState"

guy = None
bg = None







def enter():
    global guy, bg, wall, map
    guy = Guy()
    map = create_map()
    bg = Background()
    guy.set_bg(bg)
    for wall in map:
        wall.set_bg(bg)




def exit():
    global guy, bg
    del(guy)
    del(bg)




def pause():
    pass


def resume():
    pass



def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else :
            guy.handle_events(event)
        #elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            #game_framework.push_state(pause_state)


def create_map():
    map = []
    for i in range(1,3):
        wall = Wall()
        wall.x = 500
        wall.y = 25*i*2
        map.append(wall)

    for i in range(1,3):
        wall = Wall()
        wall.x = 550
        wall.y = 25*i*2
        map.append(wall)

    for i in range(1,4):
        wall = Wall()
        wall.x = 700
        wall.y = 25*i*2
        map.append(wall)

    for i in range(2,4):
        wall = Wall()
        wall.x = 900
        wall.y = 25*i*2
        map.append(wall)
    for i in range(0,20):
        wall = Wall()
        wall.x = 25*i*2 + 100
        wall.y = 0
        map.append(wall)

    for i in range(0,20):
        wall = Wall()
        wall.x = 100
        wall.y = 25*i*2
        map.append(wall)

    for i in range(0,20):
        wall = Wall()
        wall.x = 25*i*2 + 100
        wall.y = 1000
        map.append(wall)

    for i in range(0,20):
        wall = Wall()
        wall.x = 1100
        wall.y = 25*i*2
        map.append(wall)
    return map

def collide(a, b):
    collision = 0
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    #if guy.position == guy.Bottom:
    #    if guy.x >= left_b and guy.x < right_b  and bottom_a < top_b and top_a > bottom_b:
    #elif guy.position == guy.Right:
    #    if guy.x >= left_b and guy.x < right_b  and bottom_a < top_b and top_a > bottom_b:
    #elif guy.position == guy.Top:
    #    if guy.x >= left_b and guy.x < right_b and bottom_a < top_b and top_a > bottom_b:
    #elif guy.position == guy.Left:
    #    if guy.x >= left_b and guy.x < right_b and bottom_a < top_b and top_a > bottom_b:
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False



    if bottom_a < top_b and bottom_a > top_b-20: collision += 1 #블록 상
    if right_a > left_b and right_a < left_b+20: collision += 2 #블록 좌
    if top_a > bottom_b and top_a < bottom_b+20: collision += 4 #블록 하
    if left_a < right_b and left_a > right_b-20: collision += 8 #블록 우
    return collision



def update(frame_time):
    guy.update(frame_time)
    bg.update(frame_time)

    for wall in map:
        wall.update(frame_time)
        if(collide(guy,wall) > 0):
            print("Guy %d, %d, Wall %d, %d : %d" % (guy.x, guy.y, wall.x, wall.y, collide(guy, wall)))
        if guy.position == guy.BOTTOM:
            if wall.y  > guy.y - 75 and wall.y < guy.y + 75 and collide(guy,wall) == 2:
                guy.x = wall.x - 50
            if wall.x >= guy.x - 25 and wall.x < guy.x + 25 and collide(guy, wall) in (1, 3, 9) :
                guy.y = wall.y + 75
                guy.falling = False

        if guy.position == guy.RIGHT and collide(guy, wall) in (2, 3, 6):
            guy.x = wall.x - 75
            guy.falling = False
        if guy.position == guy.TOP and collide(guy, wall)in (4, 6, 12):
            guy.y = wall.y - 75
            guy.falling = False
        if guy.position == guy.LEFT and collide(guy, wall)in (8, 9, 12):
            guy.x = wall.x + 75
            guy.falling = False





def draw(frame_time):
    clear_canvas()
    bg.draw()
    for wall in map:
        wall.draw()
    guy.draw()
    guy.draw_bb()
    update_canvas()





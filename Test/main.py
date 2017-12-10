import random

import game_framework
from pico2d import *


from death import Death
from guy import Guy
from wall import Wall
from portal import Portal
from clear import Clear

from background import Background
name = "MainState"

guy = None
bg = None







def enter():
    global guy, bg, wall, map, death, portal, clear


    guy = Guy()
    portal = Portal()
    map = create_map()
    bg = Background()
    death = Death()

    clear = Clear()
    guy.set_bg(bg)
    bg.set_guy(guy)
    death.set_bg(bg)
    death.set_guy(guy)
    clear.set_bg(bg)
    clear.set_guy(guy)
    portal.set_bg(bg)
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
    map_file = open('tile.txt', 'r')
    map_data = json.load(map_file)
    map_file.close()
    count = 0

    if guy.stage == 1:
        guy.x, guy.initx = 150
        guy.y, guy.inity = 100




        wall = Wall()
        wall.x = 1200
        wall.y = 450
        map.append(wall)

        wall = Wall()
        wall.x = 1200
        wall.y = 400
        map.append(wall)

        wall = Wall()
        wall.x = 1200
        wall.y = 350
        map.append(wall)

        wall = Wall()
        wall.x = 1200
        wall.y = 300
        map.append(wall)

        wall = Wall()
        wall.x = 1250
        wall.y = 450
        wall.shape = 4
        map.append(wall)

        wall = Wall()
        wall.x = 1250
        wall.y = 400
        wall.shape = 4
        map.append(wall)

        wall = Wall()
        wall.x = 1250
        wall.y = 350
        wall.shape = 4
        map.append(wall)

        wall = Wall()
        wall.x = 1250
        wall.y = 300
        wall.shape = 4
        map.append(wall)

        wall = Wall()
        wall.x = 1750
        wall.y = 100
        map.append(wall)

        wall = Wall()
        wall.x = 600
        wall.y = 100
        map.append(wall)

        for i in range(0,100):
            wall = Wall()
            wall.x = 50*i + 100
            wall.y = 0
            map.append(wall)

        for i in range(0,10):
            wall = Wall()
            wall.x = 100
            wall.y = 50*i
            map.append(wall)

        for i in range(0,100):
            wall = Wall()
            wall.x = 25*i*2 + 100
            wall.y = 500
            map.append(wall)

        for i in range(0,10):
            wall = Wall()
            wall.x = 2000
            wall.y = 50*i
            map.append(wall)
        return map
    elif guy.stage == 2:
        for tile in map_data:
            if tile in range (1,6):
                wall = Wall()
                wall.idx = count
                wall.x = 25 + 50 * (wall.idx%30)         + 1000
                wall.y = 25 + 50 * (29 - wall.idx//30)   + 1000
                if tile == 2:
                    wall.shape = wall.DOWN
                if tile == 3:
                    wall.shape = wall.LEFT
                if tile == 4:
                    wall.shape = wall.RIGHT
                if tile == 5:
                    wall.shape = wall.UP

                map.append(wall)
            elif tile == 6:

                portal.x = 25 + 50 * (count % 30) + 1000
                portal.y = 75 + 50 * (29 - count // 30) + 1000

            elif tile == 7:

                portal.x = -25 + 50 * (count % 30) + 1000
                portal.y = 25 + 50 * (29 - count // 30) + 1000

            elif tile == 8:


                guy.initx = 25 + 50 * (count % 30) + 1000
                guy.inity = 50 + 50 * (29 - (count // 30)) + 1000
                guy.x = guy.initx
                guy.y = guy.inity
            count += 1

        return map
def collide(a, b):

    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()


    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False


    return True



def update(frame_time):

    guy.update(frame_time)
    portal.update(frame_time)
    death.update(frame_time)
    clear.update(frame_time)
    bg.update(frame_time)

    if portal.dir == 0 and guy.position in (guy.BOTTOM, guy.TOP) and collide(guy, portal):
        guy.clear = True
    elif portal.dir == 1 and guy.position in (guy.RIGHT, guy.LEFT) and collide(guy, portal):
        guy.clear = True



    NOT = 0
    BOTTOM = 1
    RIGHT = 2
    TOP = 3
    LEFT = 4
    ALL = 5
    fcount = 0
    count = 0

    for wall in map:
        wall.update(frame_time)
        dir = NOT
        if guy.position == guy.BOTTOM:
            if guy.x > wall.x - 50 and guy.x < wall.x + 50 and guy.y <= wall.y + 75 and guy.y > wall.y + 51:
                dir = BOTTOM
            elif guy.x > wall.x - 50 and guy.x < wall.x + 50 and guy.y > wall.y - 75 and guy.y < wall.y - 55 and guy.action == guy.JUMP:
                dir = TOP
            elif guy.x > wall.x - 50 and guy.x < wall.x + 50 and guy.y > wall.y - 50 and guy.y < wall.y - 35 and guy.action == guy.SPIN:
                dir = TOP
            elif guy.x >= wall.x - 50 and guy.x <= wall.x - 35 and guy.y > wall.y - 75 and guy.y <  wall.y + 75:
                dir = RIGHT

        elif guy.position == guy.RIGHT:
            if guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x >= wall.x - 75 and guy.x <  wall.x - 51:
                dir = RIGHT
            elif guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x < wall.x + 75 and guy.x >  wall.x + 55 and guy.action == guy.JUMP:
                dir = LEFT
            elif guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x < wall.x + 50 and guy.x >  wall.x + 35 and guy.action == guy.SPIN:
                dir = LEFT
            elif guy.y >= wall.y - 50 and guy.y <= wall.y - 35 and guy.x < wall.x + 75 and guy.x > wall.x - 75:
                dir = TOP

        elif guy.position == guy.TOP:
            if guy.x >  wall.x - 50 and guy.x < wall.x + 50 and guy.y >=  wall.y - 75 and guy.y < wall.y - 51:
                dir = TOP
            elif guy.x > wall.x - 50 and guy.x < wall.x + 50 and guy.y < wall.y + 75 and guy.y > wall.y + 55 and guy.action == guy.JUMP:
                dir = BOTTOM
            elif guy.x > wall.x - 50 and guy.x < wall.x + 50 and guy.y < wall.y + 50 and guy.y > wall.y + 35 and guy.action == guy.SPIN:
                dir = BOTTOM
            elif guy.x >= wall.x + 35 and guy.x <= wall.x + 50 and guy.y > wall.y - 75 and guy.y <  wall.y + 75:
                dir = LEFT

        elif guy.position == guy.LEFT:
            if guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x <= wall.x + 75 and guy.x >  wall.x + 51:
                dir = LEFT
            elif guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x > wall.x - 75 and guy.x <  wall.x - 55 and guy.action == guy.JUMP:
                dir = RIGHT
            elif guy.y > wall.y - 50 and guy.y < wall.y + 50 and guy.x > wall.x - 50 and guy.x <  wall.x - 35 and guy.action == guy.SPIN:
                dir = RIGHT
            elif guy.y <= wall.y + 50 and guy.y >= wall.y + 35 and guy.x < wall.x + 75 and guy.x > wall.x - 75:
                dir = BOTTOM

        #if wall.x >= guy.x - 50 and wall.x <= guy.x + 50 and wall.y > guy.y - 75 and wall.y < guy.y + 75:
        if(dir > 0):
            print("Guy %d, %d, Wall %d, %d : dir %d, stop %d, jumping %d, falling %d, fcount %d" % (guy.x, guy.y, wall.x, wall.y, dir, guy.stop, guy.jumping,  guy.falling, fcount))
        if guy.position == guy.BOTTOM:
            if dir == RIGHT and guy.stop == False and collide(guy, wall):
                guy.x = wall.x - 50
                guy.stop = True
                if wall.shape == wall.LEFT:
                    guy.death = True
            elif dir == RIGHT and guy.action != guy.SPIN and guy.stop == True and collide(guy, wall) == False:
                guy.stop = False
            if dir == BOTTOM and collide(guy, wall):
                if guy.action == guy.JUMP and guy.frame > 1:
                    guy.frame = 7
                guy.y = wall.y + 75

                guy.falling = False
                fcount += 1
                if wall.shape == wall.UP and guy.frame > 1:
                    guy.death = True

            if dir == TOP and collide(guy, wall):
                if wall.shape == wall.DOWN:
                    guy.death = True
                if guy.action == guy.JUMP:
                    guy.frame = 7
                    guy.y = wall.y - 75
                elif guy.action == guy.SPIN:
                    guy.frame = 6
                    guy.y = wall.y - 52



        elif guy.position == guy.RIGHT:
            if dir == TOP and guy.stop == False and collide(guy, wall):
                guy.y = wall.y - 50
                guy.stop = True
                if wall.shape == wall.DOWN:
                    guy.death = True
            elif dir == TOP and guy.action != guy.SPIN and guy.stop == True and collide(guy, wall) == False:
                guy.stop = False
            if dir == RIGHT and collide(guy, wall):
                if guy.action == guy.JUMP and guy.frame > 1:
                    guy.frame = 7
                guy.x = wall.x - 75
                guy.falling = False
                fcount += 1
                if wall.shape == wall.LEFT and guy.frame > 1:
                    guy.death = True
            if dir == LEFT and collide(guy, wall):
                if wall.shape == wall.RIGHT:
                    guy.death = True
                if guy.action == guy.JUMP:
                    guy.frame = 7
                    guy.x = wall.x + 75
                elif guy.action == guy.SPIN:
                    guy.frame = 6
                    guy.x = wall.x + 52

        elif guy.position == guy.TOP:
            if dir == LEFT and guy.stop == False and collide(guy, wall):
                guy.x = wall.x + 50
                guy.stop = True
                if wall.shape == wall.RIGHT:
                    guy.death = True
            elif dir == LEFT and guy.action != guy.SPIN and guy.stop == True and collide(guy, wall) == False:
                guy.stop = False
            if dir == TOP and collide(guy, wall):
                if guy.action == guy.JUMP and guy.frame > 1:
                    guy.frame = 7
                guy.y = wall.y - 75
                guy.falling = False
                fcount += 1
                if wall.shape == wall.DOWN and guy.frame > 1:
                    guy.death = True
            if dir == BOTTOM and collide(guy, wall):
                if wall.shape == wall.UP:
                    guy.death = True
                if guy.action == guy.JUMP:
                    guy.frame = 7
                    guy.y = wall.y + 75
                elif guy.action == guy.SPIN:
                    guy.frame = 6
                    guy.y = wall.y + 52

        elif guy.position == guy.LEFT:
            if dir == BOTTOM and guy.stop == False and collide(guy, wall):
                guy.y = wall.y + 50
                guy.stop = True
                if wall.shape == wall.UP:
                    guy.death = True
            elif dir == BOTTOM and guy.action != guy.SPIN and guy.stop == True and collide(guy, wall) == False:
                guy.stop = False
            if dir == LEFT and collide(guy, wall):
                if guy.action == guy.JUMP and guy.frame > 1:
                    guy.frame = 7
                guy.x = wall.x + 75
                guy.falling = False
                fcount += 1
                if wall.shape == wall.RIGHT and guy.frame > 1:
                    guy.death = True
            if dir == RIGHT and collide(guy, wall):
                if wall.shape == wall.LEFT:
                    guy.death = True
                if guy.action == guy.JUMP:
                    guy.frame = 7
                    guy.x = wall.x - 75
                elif guy.action == guy.SPIN:
                    guy.frame = 6
                    guy.x = wall.x - 52


        if collide(guy, wall):
            count += 1



    if fcount == 0 and guy.jumping == False:
        guy.falling = True
        if count == 0:
            guy.stop = False

    if count:
        guy.get_collision(True)
    else:
        guy.get_collision(False)





def draw(frame_time):
    clear_canvas()
    bg.draw()
    for wall in map:
        wall.draw()
    portal.draw()
    guy.draw()
    guy.draw_bb()
    clear.draw()
    death.draw()
    update_canvas()







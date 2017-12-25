from pico2d import *



class Guy:
    PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
    RUN_SPEED_KMPH = 25.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

    JUMP_SPEED_KMPH = 50.0  # Km / Hour
    JUMP_SPEED_MPM = (JUMP_SPEED_KMPH * 1000.0 / 60.0)
    JUMP_SPEED_MPS = (JUMP_SPEED_MPM / 60.0)
    JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)



    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    RUN_FPA = 6  # Frames Per Action
    JUMP_FPA = 8
    SPIN_FPA = 7

    font = None

    jumping = False
    falling = True

    stop = False
    death = False
    clear = False

    rdis = None
    jdis = None

    jump_sound = None

    RUN, JUMP, SPIN = 0, 1, 2
    TOP, BOTTOM, LEFT, RIGHT = 6, 0, 9, 3
    action, position = RUN, BOTTOM

    def __init__(self):
        self.initx, self.inity = 0, 0
        self.x, self.y = self.initx, self.inity
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('guy.png')
        self.xdir = 0
        self.ydir = 0
        self.sound = 1
        self.stage = 1
        self.deathcount = 0
        self.redraw = 0
        self.ending = 0

        if Guy.font == None:
            Guy.font = load_font('ENCR10B.TTF', 25)
        if Guy.jump_sound == None:
            Guy.jump_sound = load_wav('jump.wav')
            Guy.jump_sound.set_volume(40)

    def set_bg(self, bg):
        self.bg = bg

    def get_collision(self, col):
        self.col = col

    def update(self, frame_time):
        if self.sound == 0:
            self.jump_sound.play()

        self.sound = 1

        if self.death == True or self.clear == True:

            self.jumping = True
            self.stop = True
            self.falling = False
            self.rdis = 0
            self.jdis = 0
        else:
            self.rdis = Guy.RUN_SPEED_PPS * frame_time
            self.jdis = Guy.JUMP_SPEED_PPS * frame_time



        if self.position == self.BOTTOM:
            self.xdir = 1
            self.ydir = 1
        elif self.position == self.RIGHT:
            self.xdir = -1
            self.ydir = 1
        elif self.position == self.TOP:
            self.xdir = -1
            self.ydir = -1
        elif self.position == self.LEFT:
            self.xdir = 1
            self.ydir = -1

        if self.stop == False:

            if self.position in (self.TOP, self.BOTTOM):
                self.x += self.rdis * self.xdir
            else:
                self.y += self.rdis * self.ydir

        if self.action == self.RUN:
            self.total_frames += Guy.RUN_FPA * Guy.ACTION_PER_TIME * frame_time
            self.frame = int(self.total_frames) % Guy.RUN_FPA

        elif self.action == self.JUMP:
            if self.jumping == False:
                self.jumping = True
                self.falling = False
                self.total_frames = 0
                self.frame = 0

            else:
                if self.frame < 7:
                    self.stop = False
                    if self.frame < 3:
                        if self.position in (self.TOP, self.BOTTOM):
                            self.y += self.jdis * self.ydir
                        else:
                            self.x += self.jdis * self.xdir
                    elif self.frame > 3:
                        if self.position in (self.TOP, self.BOTTOM):
                            self.y -= self.jdis * self.ydir
                        else:
                            self.x -= self.jdis * self.xdir
                    self.total_frames += Guy.JUMP_FPA * Guy.ACTION_PER_TIME * frame_time
                    self.frame = int(self.total_frames) % Guy.JUMP_FPA
                else:
                    self.jumping = False
                    self.falling = True
                    self.action = self.RUN
                    self.total_frames = 0
                    self.frame = 0
        elif self.action == self.SPIN:
            if self.jumping == False:
                self.total_frames = 0
                self.frame = 0
                self.jumping = True
                self.falling = False
            else:
                if self.stop == True and self.frame == 5:
                    self.frame += 1
                if self.frame < 6:

                    self.stop = False

                    if self.position in (self.TOP, self.BOTTOM):
                        self.y += self.rdis * self.ydir
                    else:
                        self.x += self.rdis * self.xdir

                    self.total_frames += Guy.SPIN_FPA * Guy.ACTION_PER_TIME * frame_time
                    self.frame = int(self.total_frames) % Guy.SPIN_FPA
                else:
                    self.jumping = False
                    self.falling = True
                    self.stop = False
                    self.action = self.RUN
                    self.total_frames = 0
                    self.frame = 0
                    self.position = (self.position + 3) % 12

                    #if self.col:
                    if self.position == self.BOTTOM:
                        self.y += 25
                    if self.position == self.TOP:
                        self.y -= 25
                    if self.position == self.RIGHT:
                        self.x -= 25
                    if self.position == self.LEFT:
                        self.x += 25




        if self.falling == True and self.jumping == False:
            if self.position in (self.TOP, self.BOTTOM):
                self.y -= self.jdis * self.ydir
            else:
                self.x -= self.jdis * self.xdir


        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)

    def draw(self):
        Guy.font.draw(self.initx - self.bg.window_left, self.inity + 175 - self.bg.window_bottom, 'Death Counter = %d'%(self.deathcount), (255,0,0) )


        if self.image != None:
            if self.jumping == False and self.falling == True:
                self.image.clip_draw(500, (10 - self.position) * 100, 100, 100,
                                 self.x - self.bg.window_left, self.y - self.bg.window_bottom)
            elif self.stop == True and self.jumping == False:
                self.image.clip_draw(700, (10 - self.position) * 100, 100, 100,
                                 self.x - self.bg.window_left, self.y - self.bg.window_bottom)
            else:
                self.image.clip_draw(self.frame * 100, (11 - self.action - self.position) * 100, 100, 100,
                             self.x - self.bg.window_left, self.y - self.bg.window_bottom)


    def get_bb(self):

            if self.position in (self.TOP, self.BOTTOM):
                return self.x - 25 - self.bg.window_left, self.y - 50 - self.bg.window_bottom, self.x + 25 - self.bg.window_left, self.y + 50 - self.bg.window_bottom
            else:
                return self.x - 50 - self.bg.window_left, self.y - 25 - self.bg.window_bottom, self.x + 50 - self.bg.window_left, self.y + 25 - self.bg.window_bottom

    def draw_bb(self):
        pass
        #draw_rectangle(*self.get_bb())

    def handle_events(self, event):
        if self.falling == False and self.death == False:
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and self.jumping == False:
                self.action = self.JUMP
                self.sound = 0
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and self.jumping == True  and self.frame < 3:
                self.action = self.SPIN

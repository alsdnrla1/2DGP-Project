from pico2d import *
from background import Background


class Guy:
    PIXEL_PER_METER = (10.0 / 0.2)  # 10 pixel 20 cm
    RUN_SPEED_KMPH = 20.0  # Km / Hour
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

    jumping = False
    falling = True
    RUN, JUMP, SPIN = 0, 1, 2
    TOP, BOTTOM, LEFT, RIGHT = 6, 0, 9, 3
    action, position = RUN, BOTTOM

    def __init__(self):
        self.x, self.y = 300, 200
        self.frame = 0
        self.total_frames = 0
        self.image = load_image('guy.png')
        self.xdir = 0
        self.ydir = 0

    def set_bg(self, bg):
        self.bg = bg

    def update(self, frame_time):
        rdis = Guy.RUN_SPEED_PPS * frame_time
        jdis = Guy.JUMP_SPEED_PPS * frame_time

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

        if self.position in (self.TOP, self.BOTTOM):
            self.x += rdis * self.xdir
        else:
            self.y += rdis * self.ydir

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

                    if self.frame < 2:
                        if self.position in (self.TOP, self.BOTTOM):
                            self.y += jdis * self.ydir
                        else:
                            self.x += jdis * self.xdir
                    elif self.frame > 4:
                        if self.position in (self.TOP, self.BOTTOM):
                            self.y -= jdis * self.ydir
                        else:
                            self.x -= jdis * self.xdir
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
                if self.frame < 6:
                    if self.position in (self.TOP, self.BOTTOM):
                        self.x += rdis * self.ydir
                        self.y += rdis * self.ydir
                    else:
                        self.y += rdis * self.ydir
                        self.x += rdis * self.xdir

                    self.total_frames += Guy.SPIN_FPA * Guy.ACTION_PER_TIME * frame_time
                    self.frame = int(self.total_frames) % Guy.SPIN_FPA
                else:
                    self.jumping = False
                    self.falling = True
                    self.action = self.RUN
                    self.total_frames = 0
                    self.frame = 0
                    self.position = (self.position + 3) % 12

        if self.falling == True and self.jumping == False:
            if self.position in (self.TOP, self.BOTTOM):
                self.y -= jdis * self.ydir
            else:
                self.x -= jdis * self.xdir


        self.x = clamp(0, self.x, self.bg.w)
        self.y = clamp(0, self.y, self.bg.h)

    def draw(self):
        self.image.clip_draw(self.frame * 100, (11 - self.action - self.position) * 100, 100, 100,
                             self.x - self.bg.window_left, self.y - self.bg.window_bottom)

    def get_bb(self):
        if self.action == self.SPIN:
            return self.x - 25 - self.bg.window_left, self.y - 25 - self.bg.window_bottom, self.x + 25 - self.bg.window_left, self.y + 25 - self.bg.window_bottom
        else:
            if self.position in (self.TOP, self.BOTTOM):
                return self.x - 25 - self.bg.window_left, self.y - 50 - self.bg.window_bottom, self.x + 25 - self.bg.window_left, self.y + 50 - self.bg.window_bottom
            else:
                return self.x - 50 - self.bg.window_left, self.y - 25 - self.bg.window_bottom, self.x + 50 - self.bg.window_left, self.y + 25 - self.bg.window_bottom

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handle_events(self, event):
        if self.falling == False:
            if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and self.jumping == False:
                self.action = self.JUMP
            elif event.type == SDL_KEYDOWN and event.key == SDLK_c and self.jumping == False:
                self.action = self.SPIN
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE and self.jumping == True and self.frame < 3:
                self.action = self.SPIN

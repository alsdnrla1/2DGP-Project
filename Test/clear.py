from pico2d import *

class Clear:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAME_PER_ACTION = 12  # Frames Per Action

    def set_guy(self, guy):
        self.guy = guy
    def set_bg(self, bg):
        self.bg = bg

    def __init__(self):
        self.x, self.y = 0, 0
        self.frame = 0
        self.height = 0
        self.total_frames = 0
        self.reverse = 1

    def update(self, frame_time):
        self.x = self.guy.x
        self.y = self.guy.y
        if self.image == None:

            self.image = load_image('portal_animation1.png')
        if self.guy.clear == True:




            self.total_frames += Clear.FRAME_PER_ACTION * Clear.ACTION_PER_TIME * frame_time
            self.frame = int(self.total_frames) % Clear.FRAME_PER_ACTION

            if self.height == 2 and self.frame == 0:
                self.guy.image = None

            if self.frame == 4:
                self.height += 1
                self.frame = 0
                self.total_frames = 0

            if self.height == 8:
                self.height = 0
                self.guy.death = False
                self.guy.jumping = False
                self.guy.falling = True
                self.guy.stop = False
                self.guy.clear = False
                self.guy.x = 150
                self.guy.y = 75
                self.guy.action = self.guy.RUN
                self.guy.position = self.guy.BOTTOM
                self.guy.image = load_image('guy.png')



    def draw(self):
        if self.guy.clear == True:
            self.image.clip_draw((self.frame % 4) * 200, (3-self.height) * 200, 200, 200, self.x - self.bg.window_left, self.y - self.bg.window_bottom)



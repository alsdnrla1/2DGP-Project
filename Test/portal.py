from pico2d import *

class Portal:
    image = None

    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAME_PER_ACTION = 15  # Frames Per Action

    def set_guy(self, guy):
        self.guy = guy
    def set_bg(self, bg):
        self.bg = bg

    def __init__(self):
        self.x, self.y = 600, 400
        self.frame = 0
        self.height = 0
        self.total_frames = 0
        self.dir = 0
    def get_bb(self):
        return self.x - 1 - self.bg.window_left, self.y - 1- self.bg.window_bottom, self.x + 1- self.bg.window_left, self.y + 1- self.bg.window_bottom
    def update(self, frame_time):

        if self.image == None:
            if self.dir:
                self.image = load_image('portal1.png')
            else:
                self.image = load_image('portal.png')





        self.total_frames += Portal.FRAME_PER_ACTION * Portal.ACTION_PER_TIME * frame_time
        self.frame = int(self.total_frames) % Portal.FRAME_PER_ACTION



        if self.frame == 5:
            self.height += 1
            self.frame = 0
            self.total_frames = 0

        if self.height == 3:
            self.height = 0




    def draw(self):

        self.image.clip_draw((self.frame % 5) * 75, (2-self.height) * 150, 75, 150, self.x - self.bg.window_left, self.y - self.bg.window_bottom)


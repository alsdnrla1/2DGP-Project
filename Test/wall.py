from pico2d import *

class Wall:
    image = None
    shape = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    RIGHT = 4
    def __init__(self):
        self.x, self.y = 25, 25

    def set_bg(self, bg):
        self.bg = bg

    def get_bb(self):
        return self.x - 25 - self.bg.window_left, self.y - 25- self.bg.window_bottom, self.x + 25- self.bg.window_left, self.y + 25- self.bg.window_bottom
    def update(self, frame_time):
        if self.image == None:
            if self.shape == 0:
                self.image = load_image('block.png')
            if self.shape == self.UP:
                self.image = load_image('up_spike.png')
            if self.shape == self.RIGHT:
                self.image = load_image('right_spike.png')
            if self.shape == self.DOWN:
                self.image = load_image('down_spike.png')
            if self.shape == self.LEFT:
                self.image = load_image('left_spike.png')

    def draw(self):
        self.image.draw(self.x - self.bg.window_left, self.y - self.bg.window_bottom)


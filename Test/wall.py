from pico2d import *

class Wall:
    image = None

    def __init__(self):
        self.x, self.y = 25, 25

    def set_bg(self, bg):
        self.bg = bg

    def get_bb(self):
        return self.x - 25 - self.bg.window_left, self.y - 25- self.bg.window_bottom, self.x + 25- self.bg.window_left, self.y + 25- self.bg.window_bottom
    def update(self, frame_time):
        if self.image == None:
            self.image = load_image('block.png')

    def draw(self):
        self.image.draw(self.x - self.bg.window_left, self.y - self.bg.window_bottom)
        #for i in range(1,50):
            #self.image.draw(self.x * 2 * i - self.bg.window_left, self.y - self.bg.window_bottom)
            #self.image.draw(self.x + 800 - self.bg.window_left, self.y * 2 * i - self.bg.window_bottom)

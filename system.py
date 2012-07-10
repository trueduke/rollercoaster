from nodebox.graphics import *

class System(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scale = 10
        self.x = width/2
        self.y = height/2

    def draw(self):
        # first draw grid
        stroke(0.9)
        for x in range(self.x, 0, -self.scale):
            line(x, 0, x, self.height)
        for x in range(self.x, self.width, self.scale):
            line(x, 0, x, self.height)

        for y in range(self.y, 0, -self.scale):
            line(0, y, self.width, y)
        for y in range(self.y, self.width, self.scale):
            line(0, y, self.width, y)

        # then draw axes
        stroke(0.5)

        line(self.x, 0, self.x, self.height)
        line(0, self.y, self.width, self.y)

    def get_screen_x(self, x):
        '''get screen x coordinate for x in system'''
        return self.scale*x + self.x

    def get_screen_y(self, y):
        '''get screen y coordinate for y in system'''
        return self.scale*y + self.y

    def get_screen_dim(self, dim):
        return self.scale*dim

    def get_system_x(self, x):
        '''get system x coordinate for x on screen'''
        return float((x - self.x))/float(self.scale)

    def get_system_y(self, y):
        '''get system y coordinate for y on screen'''
        return float((y - self.y))/float(self.scale)

    def get_system_dim(self, dim):
        return float(dim)/float(self.scale)

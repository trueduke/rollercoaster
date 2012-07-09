import os, sys; sys.path.insert(0, "..")
from nodebox.graphics import *

from math import *

import Box2D as physics


class Equation(object):
    def __init__(self, world):
        eq_s = "x*x/40.0 if x >0 else -x"
        self.eq = compile(eq_s, '<string>', 'eval')


        self.verts = [(x, self.calc(x)) for x in range(-100, 100, 1)]
        # new_ones = [(vert[0]-0.1, vert[1]-0.1) for vert in reversed(self.verts)]
        # self.verts += new_ones

        # bd = physics.b2BodyDef()
        # bd.position = (0.0, 0.0)
        # self.body = world.CreateBody(bd)
        
        # edgeDef = physics.b2EdgeChainDef()
        # edgeDef.setVertices_tuple(self.verts)
        # edgeDef.isALoop = False
        # edgeDef.density = 0
        # self.shape = self.body.CreateShape(edgeDef)

        # self.body.SetMassFromShapes()

        # self.shape.friction = 0
        # self.shape.restitution = 1.0

        for i, vert in enumerate(self.verts):
            if i==0 or i==len(self.verts)-1:
                continue

            bd = physics.b2BodyDef()
            bd.position = (vert[0], vert[1])
            body = world.CreateBody(bd)
            
            edgeDef = physics.b2PolygonDef()
            v = [(self.verts[i-1][0]-vert[0], self.verts[i-1][1]-vert[1]), (0,0), (self.verts[i+1][0]-vert[0], self.verts[i+1][1]-vert[1])]
            edgeDef.setVertices(v)
            shape = body.CreateShape(edgeDef)

            body.mass = 0

    def update(self):
        pass

    def calc(self, x):
        # ret = x*x/40.0 if x >0 else -x
        ret = eval(self.eq)
        ret = min(100, ret)
        return float(ret)

    def draw(self, system):
        prev_x, prev_y = None, None
        for screen_x in range(system.width):
            x = system.get_system_x(screen_x)
            y = self.calc(x)
            screen_y = system.get_screen_y(y)
            if None not in [prev_x, prev_y]:
                line(system.get_screen_x(prev_x), system.get_screen_y(prev_y), screen_x, screen_y)
            else:
                rect(screen_x, screen_y, 1, 1)
            prev_x = x
            prev_y = y

        fill (0)
        # for x, y in self.verts:
        #     ellipse(system.get_screen_x(x), system.get_screen_y(y), 10, 10)

        # for i, vert in enumerate(self.verts):
        #     if i==0 or i==len(self.verts)-1:
        #         continue

        #     x0, y0 = (self.verts[i-1][0], self.verts[i-1][1])
        #     x1, y1 = (vert[0], vert[1])
        #     x2, y2 = (self.verts[i+1][0], self.verts[i+1][1])
        #     line(system.get_screen_x(x0),system.get_screen_y(y0), system.get_screen_x(x1), system.get_screen_y(y1))
        #     line(system.get_screen_x(x1),system.get_screen_y(y1), system.get_screen_x(x2), system.get_screen_y(y2))


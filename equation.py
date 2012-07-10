from nodebox.graphics import *
from math import *
import Box2D as physics

DEBUG = False


class Equation(object):
    def __init__(self, world):
        # the equation is an expression given by the player
        self.expression_string = "x*x/40.0 if x >0 else -x"
        # expression_string = "x*x/40.0"
        # we compile it to call it quickly from the calc function
        self.expression = compile(self.expression_string, '<string>', 'eval')

        
        # now we have to build it in the world
        self.world = world
        self.initialize_bodies()

    def initialize_bodies(self):
        # first, calculate the points/vertices
        self.verts = [(x, self.calc(x)) for x in range(-200, 200, 1)]

        # for each triplet of vertices, we create a body linking them
        self.bodies = []
        for i, vert in enumerate(self.verts):
            if i==0 or i==len(self.verts)-1:
                continue

            bd = physics.b2BodyDef()
            bd.position = (vert[0], vert[1])
            body = self.world.CreateBody(bd)
            
            edgeDef = physics.b2PolygonDef()
            v = [(self.verts[i-1][0]-vert[0], self.verts[i-1][1]-vert[1]) ,(0,0), (self.verts[i+1][0]-vert[0], self.verts[i+1][1]-vert[1])]
            edgeDef.setVertices(v)
            shape = body.CreateShape(edgeDef)

            # for a fixed body, mass has to be zero
            shape.friction = 1.0
            body.mass = 0

            self.bodies.append(body)


    def reset(self):
        self.expression = compile(self.expression_string, '<string>', 'eval')
        for body in self.bodies:
            self.world.DestroyBody(body)
        self.initialize_bodies()


    def calc(self, x):
        ret = eval(self.expression)
        ret = min(100, ret)
        return float(ret)

    def update(self):
        pass

    def draw(self, system):
        if not DEBUG:
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

        if DEBUG:
            fill (0)
            # for x, y in self.verts:
            #     ellipse(system.get_screen_x(x), system.get_screen_y(y), 10, 10)

            for i, vert in enumerate(self.verts):
                if i==0 or i==len(self.verts)-1:
                    continue

                x0, y0 = (self.verts[i-1][0], self.verts[i-1][1])
                x1, y1 = (vert[0], vert[1])
                x2, y2 = (self.verts[i+1][0], self.verts[i+1][1])
                line(system.get_screen_x(x0),system.get_screen_y(y0), system.get_screen_x(x1), system.get_screen_y(y1))
                line(system.get_screen_x(x1),system.get_screen_y(y1), system.get_screen_x(x2), system.get_screen_y(y2))


from nodebox.graphics import *
from math import sin, cos
import Box2D as physics


class Ball(object):
    def __init__(self, world, x0, y0, theta0):
        # constants
        self.radius = 4

        # coordinates for drawing
        self.theta = theta0
        self.x = x0
        self.y = y0
        
        # first define a body
        bodyDef = physics.b2BodyDef()
        bodyDef.position = (self.x, self.y)
        # create body in our world
        self.body = world.CreateBody(bodyDef)

        # then define the attached shape
        # (it's a circle)
        shapeDef = physics.b2CircleDef()
        shapeDef.radius = self.radius
        shapeDef.density = 3
        # create the shape
        self.shape = self.body.CreateShape(shapeDef)
        # attach a mass
        self.body.SetMassFromShapes()

        # fixtures
        self.shape.friction = 1.0
        self.shape.restitution = 0.1

        # initial angular velocity
        self.body.angularVelocity = -30.0

    def update(self):
        # drawing pos equals body pos
        self.x = self.body.position.x
        self.y = self.body.position.y
        self.theta = self.body.angle

    def draw(self, system):
        x = system.get_screen_x(self.x)
        y = system.get_screen_y(self.y)
        r = system.get_screen_dim(self.radius)

        nostroke()
        fill(0.0, 0.5, 0.75, 0.5)
        ellipse(x, y, r*2, r*2)
        fill(0)
        stroke(0)
        line(x, y, x+cos(self.theta)*r, y+sin(self.theta)*r)

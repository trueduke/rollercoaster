from nodebox.graphics import *
from ball import Ball
from system import System
from equation import Equation
import Box2D as physics

# define a world
worldAABB=physics.b2AABB()
# it's a big one
worldAABB.lowerBound = (-1000, -1000)
worldAABB.upperBound = ( 1000,  1000)

# setup gravity
gravity = physics.b2Vec2(0, -50)
# let body sleep
doSleep = True

# initialize world
world = physics.b2World(worldAABB, gravity, doSleep)

# Prepare for simulation. Typically we use a time step of 1/60 of a
# second (60Hz) and 10 velocity/8 position iterations.
timeStep = 1.0 / 60
vel_iters, pos_iters = 10, 8

# for debug, show graphics coords
def show_coord():
    fill(0)
    x,y = canvas.mouse.xy
    text("%s,%s"%(x,y), x, y)

# show coords in ortho system
def show_coord_in_system(system):
    fill(0)
    x_mouse,y_mouse = canvas.mouse.xy
    x = x_mouse - system.x
    y = y_mouse - system.y
    x/=system.scale
    y/=system.scale
    text("%s,%s"%(x,y), x_mouse, y_mouse+20)

# nodebox slider plugged to the system scale
def create_scale_slider():
    from nodebox.gui import Slider
    slider = Slider(default=5.0, min=1.0, max=30.0, steps=100)
    slider.x = 10
    slider.y = 10
    canvas.append(slider)
    return slider

####

speed(60)
canvas.size = 800, 800

# our ortho system, width and height in pixels
s = System(800, 800)

# our slider
slider = create_scale_slider()

balls = []

for i in range(10):
    balls.append(Ball(world, -50, 70 + i*20, 0))

e = Equation(world)

def update():
    world.Step(timeStep, vel_iters, pos_iters)
    s.scale = int(slider.value)

    for ball in balls:
        ball.update()

    e.update()

def draw(canvas):
    # clear canvas
    canvas.clear()

    # update everything
    update()

    # draw system, balls, equation
    s.draw()
    for ball in balls:
        ball.draw(s)
    e.draw(s)

    # show different coords
    show_coord()
    show_coord_in_system(s)

    # drag view
    m = canvas.mouse
    if m.dragged:
        s.x += m.dx
        s.y += m.dy


# RUN!
canvas.run(draw)
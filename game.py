from nodebox.graphics import *
from ball import Ball
from system import System
from equation import Equation
import Box2D as physics

worldAABB=physics.b2AABB()
worldAABB.lowerBound = (-200, -200)
worldAABB.upperBound = ( 200,  200)
gravity = physics.b2Vec2(0, -100)
doSleep = True
world = physics.b2World(worldAABB, gravity, doSleep)

# groundBodyDef = physics.b2BodyDef()
# groundBodyDef.position = [0, -10]
# groundBody = world.CreateBody(groundBodyDef)
# groundShapeDef = physics.b2PolygonDef()
# groundShapeDef.SetAsBox(50, 10)
# groundBody.CreateShape(groundShapeDef)

timeStep = 1.0 / 60
vel_iters, pos_iters = 10, 8

def show_coord():
    fill(0)
    x,y = canvas.mouse.xy
    text("%s,%s"%(x,y), x, y)

def show_coord_in_system(system):
    fill(0)
    x_mouse,y_mouse = canvas.mouse.xy
    x = x_mouse - system.x
    y = y_mouse - system.y
    x/=system.scale
    y/=system.scale
    text("%s,%s"%(x,y), x_mouse, y_mouse+20)

def create_scale_slider():
    from nodebox.gui import Slider
    slider = Slider(default=5.0, min=1.0, max=30.0, steps=100)
    slider.x = 10
    slider.y = 10
    canvas.append(slider)
    return slider

s = System(800, 800)
slider = create_scale_slider()

balls = []

for i in range(10):
    balls.append(Ball(world, -50, 70 + i*20, 0))

# b = Ball(world, -30, 50, 0)
# b2 = Ball(world, -30, 70, 0)
e = Equation(world)

# w = World()
# w.add_ball(b)
# w.add_equation(e)

def draw(canvas):
    canvas.clear()

    world.Step(timeStep, vel_iters, pos_iters)

    s.scale = int(slider.value)
    s.draw()

    for ball in balls:
        ball.update()
        ball.draw(s)

    # b.update()
    # b2.update()
    # b.draw(s)
    # b2.draw(s)

    e.update()
    e.draw(s)

    # w.update()
    # w.draw(s)


    show_coord()
    show_coord_in_system(s)

    m = canvas.mouse
    if m.dragged:
        s.x += m.dx
        s.y += m.dy



speed(60)
canvas.size = 800, 800
canvas.run(draw)
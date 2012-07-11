from nodebox.graphics import *
from ball import Ball
from system import System
from equation import Equation
import Box2D as physics
from nodebox.gui import *

# define a world
worldAABB=physics.b2AABB()
# it's a big one
worldAABB.lowerBound = (-1000, -1000)
worldAABB.upperBound = ( 1000,  1000)

# setup gravity
gravity = physics.b2Vec2(0, 0)
# let body sleep
doSleep = True

# initialize our world
# global world
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
    slider = Slider(default=30.0, min=3.0, max=50.0, steps=100)
    slider.x = 10
    slider.y = 10
    # canvas.append(slider)
    return slider

# button for gravity
def create_start_button():
    button = Button("Go!", action=change_mode, x=10, y=30, width=125)
    # canvas.append(button)
    return button

# start gravity
def start_gravity(button):
    gravity = physics.b2Vec2(0, -10)
    world.gravity = gravity

# reset level
def reset_level(button):
    # here, put each ball in a mode where they go back to their initial position
    # for the moment, destroy the balls and recreate them at their init position
    destroy_balls()
    init_balls()
    gravity = physics.b2Vec2(0, 0)
    world.gravity = gravity

def change_mode(button):
    if button.caption == "Go!":
        start_gravity(button)
        button.caption = "Reset"
    elif button.caption == "Reset":
        reset_level(button)
        button.caption = "Go!"

def create_equation_field(equation):
    field = Field(value=equation.expression_string, height=70, wrap=True, hint="expression", id="field_text")
    return field

def create_equation_update_button(equation, equation_field):
    button = Button("Update", action=update_equation, x=10, y=30, width=125)
    button.associated_field = equation_field
    button.associated_equation = equation
    return button

def update_equation(button):
    button.associated_equation.expression_string = button.associated_field.value
    button.associated_equation.reset()

def create_panel(equation_field, equation_button, scale_slider, start_button):
    panel = Panel("Control Panel", width=400, height=200, fixed=False, modal=True, x=10, y=50)
    panel.append(Rows(
    [("Your\n\nequation", equation_field),
     ("Update eq", equation_button),
     ("scale", scale_slider),
     ("show grid?", Flag(default=True, id="show")),
     ("ready?", start_button),
    ], width=200))
    panel.pack()
    canvas.append(panel)
    return panel

####

speed(60)
canvas.size = 800, 800

# our ortho system, width and height in pixels
s = System(800, 800)

e = Equation(world)

# our slider
slider = create_scale_slider()
# start button
button = create_start_button()
# equation field
field = create_equation_field(e)
# equation button
equation_button = create_equation_update_button(e, field)
# panel
panel = create_panel(field, equation_button, slider, button)

balls = []

def init_balls():
    for i in range(1):
        balls.append(Ball(world, -5, 8 + i*2, 0))

def destroy_balls():
    balls_to_remove = []
    for ball in balls:
        world.DestroyBody(ball.body)
        balls_to_remove.append(ball)

    for ball in balls_to_remove:
        balls.remove(ball)

init_balls()

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
    if m.dragged and not panel.dragged:
        s.x += m.dx
        s.y += m.dy


# RUN!
canvas.run(draw)
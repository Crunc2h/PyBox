from turtle import *
import random
import math
screen_obj = Screen()
screen_obj.bgcolor("black")
screen_obj.colormode(255)

turtle_obj = Turtle()
turtle_obj.shape("circle")
turtle_obj.color("red")

turtle_obj.width(0)
turtle_obj.speed(0)
turtle_obj.shapesize(0.1)
turtle_obj.pensize(3)

turtle_obj.forward(300)
turtle_obj.home()

turtle_obj.left(90)
turtle_obj.forward(300)
turtle_obj.home()

turtle_obj.left(180)
turtle_obj.forward(300)
turtle_obj.home()

turtle_obj.left(270)
turtle_obj.forward(300)
turtle_obj.home()

turtle_obj.pensize(0.1)

def draw_polygon(turtle, apex_angle, magnitude):
    heading = turtle.heading()
    step_length = 5 + random.random() * 10
    delta_steps_count = int(magnitude / step_length / 2)
    if delta_steps_count == 0:
        delta_steps_count = 1
    delta_angle = apex_angle / delta_steps_count
    for n in range(delta_steps_count):
        turtle.left(delta_angle)
        turtle.forward(step_length)
    for n in range(delta_steps_count):
        turtle.left(delta_angle * -1)
        turtle.forward(step_length)

while True:
    turtle_obj.left(random.randint(0,360))
    turtle_obj.color("white")
    turtle_obj.setpos(0,0)
    color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    turtle_obj.color(color)
    turtle_obj.pencolor(color)
    magnitude = random.randint(10,1000)
    direction = random.choice([-1,1])
    apex_angle = random.randint(0,90) * direction
    draw_polygon(turtle_obj, apex_angle, magnitude)

draw_polygon(turtle_obj, 30, 100)















screen_obj.exitonclick()


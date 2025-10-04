from turtle import Turtle, Screen
import random

tim = Turtle()

color_list = [
    "red", "blue", "green", "yellow", "orange", "purple",
    "pink", "black", "gray", "cyan", "magenta", "brown",
    "lime", "navy", "teal", "maroon", "violet", "gold",
    "skyblue", "salmon", "coral", "khaki", "olive", "turquoise"
]

tim.penup()
tim.setheading(120)
tim.forward(100)
tim.setheading(0)
tim.forward(1)
tim.pendown()

def draw_shape(num_sides):
    angle = 360 / num_sides
    for _ in range(num_sides):
        tim.forward(100)
        tim.right(angle)

for shape_size_n in range(3, 11):
    tim.color(random.choice(color_list))
    draw_shape(shape_size_n)

screen = Screen()
screen.exitonclick()

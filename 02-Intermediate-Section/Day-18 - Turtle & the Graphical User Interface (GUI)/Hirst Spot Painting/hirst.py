import turtle as turtle_module
import random

turtle_module.colormode(255)
tim = turtle_module.Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()
color_list = [(229, 225, 221), (231, 206, 85), (218, 229, 219), (231, 222, 226), (224, 150, 89), (215, 224, 230),
              (120, 166, 185), (159, 14, 21), (34, 110, 157), (232, 82, 46), (124, 176, 144), (8, 97, 38),
              (171, 21, 16), (199, 65, 28), (185, 186, 27), (31, 128, 47), (12, 41, 74), (15, 63, 40), (242, 202, 5),
              (138, 82, 95), (85, 15, 22), (51, 166, 77), (44, 26, 22), (6, 65, 137), (173, 135, 149), (232, 170, 160),
              (48, 150, 195), (219, 66, 71), (74, 135, 186), (169, 206, 175)]


tim.setheading(225)
tim.forward(300)
tim.setheading(0)
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)


screen = turtle_module.Screen()
screen.exitonclick()

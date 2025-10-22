import turtle
import random
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Space Invaders")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)  # Turn off automatic screen updates

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

# Player movement
player_speed = 15

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bullet_speed = 20
bullet_state = "ready"  # ready - ready to fire, fire - bullet is firing

# Create enemies
number_of_enemies = 5
enemies = []

for i in range(number_of_enemies):
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_speed = 2

for enemy in enemies:
    enemy.color("red")
    enemy.shape("circle")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x
    y = enemy_start_y
    enemy.setposition(x, y)
    enemy_start_x += 100

# Create barriers
barriers = []
number_of_barriers = 4
barrier_segments = []


# Function to create a single barrier
def create_barrier(x, y):
    barrier = []
    for i in range(4):
        for j in range(3):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("green")
            segment.penup()
            segment.speed(0)
            segment.shapesize(0.5, 0.5)  # Smaller segments
            segment.setposition(x + (j * 10), y - (i * 10))
            barrier.append(segment)
    return barrier


# Create multiple barriers
barrier_positions = [-200, -100, 0, 100]
for pos in barrier_positions:
    barriers.append(create_barrier(pos, -200))

# Score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 260)
score_pen.hideturtle()
score_string = "Score: %s" % score
score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

# Game over text
game_over_pen = turtle.Turtle()
game_over_pen.speed(0)
game_over_pen.color("red")
game_over_pen.penup()
game_over_pen.hideturtle()


# Functions for player movement
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        # Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = t1.distance(t2)
    if distance < 15:
        return True
    else:
        return False


# Keyboard bindings
screen.listen()
screen.onkey(move_left, "Left")
screen.onkey(move_right, "Right")
screen.onkey(fire_bullet, "space")

# Main game loop
game_over = False
while not game_over:
    screen.update()  # Update the screen manually

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Check for boundary collision
        if enemy.xcor() > 280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1

        if enemy.xcor() < -280:
            # Move all enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemy_speed *= -1

        # Check for collision with player
        if is_collision(player, enemy):
            game_over = True
            game_over_pen.write("GAME OVER", align="center", font=("Arial", 24, "normal"))

        # Check for collision between bullet and enemy
        if is_collision(bullet, enemy):
            # Reset the bullet
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            enemy.setposition(random.randint(-200, 200), random.randint(100, 250))
            # Update the score
            score += 10
            score_string = "Score: %s" % score
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 14, "normal"))

        # Check if enemy has reached the bottom
        if enemy.ycor() < -260:
            game_over = True
            game_over_pen.write("GAME OVER", align="center", font=("Arial", 24, "normal"))

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check if bullet has reached the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bullet_state = "ready"

    # Check for collision between bullet and barriers
    for barrier in barriers:
        for segment in barrier[:]:  # Use a copy of the list for iteration
            if segment.distance(bullet) < 15:
                segment.hideturtle()
                barrier.remove(segment)
                bullet.hideturtle()
                bullet_state = "ready"

    # Check for collision between enemies and barriers
    for barrier in barriers:
        for segment in barrier[:]:
            for enemy in enemies:
                if segment.distance(enemy) < 15:
                    segment.hideturtle()
                    barrier.remove(segment)

    # Small delay to control game speed
    time.sleep(0.01)

# Keep the window open
turtle.done()

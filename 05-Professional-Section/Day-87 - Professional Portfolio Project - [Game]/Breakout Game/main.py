import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
BACKGROUND = (20, 20, 40)
PADDLE_COLOR = (0, 180, 255)
BALL_COLOR = (255, 255, 255)
BRICK_COLORS = [
    (255, 0, 0),  # Red
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
]
TEXT_COLOR = (255, 255, 255)

# Game elements
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS, BRICK_COLS = 5, 9
BRICK_GAP = 5

# Game variables
score = 0
lives = 3
level = 1
game_state = "start"  # start, playing, game_over, win

# Clock for controlling game speed
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont(None, 36)


# Generate sound effects programmatically
def generate_beep_sound(frequency=440, duration=100):
    sample_rate = 44100
    n_samples = int(round(duration * 0.001 * sample_rate))

    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)
    max_sample = 2 ** (16 - 1) - 1

    for s in range(n_samples):
        t = float(s) / sample_rate
        buf[s][0] = int(max_sample * math.sin(2 * math.pi * frequency * t))
        buf[s][1] = int(max_sample * math.sin(2 * math.pi * frequency * t))

    sound = pygame.sndarray.make_sound(buf)
    return sound


# Try to generate sounds, if numpy is available
try:
    import numpy

    pong_sound = generate_beep_sound(440, 50)
    score_sound = generate_beep_sound(880, 100)
except ImportError:
    # If numpy is not available, create silent sounds
    pong_sound = pygame.mixer.Sound(pygame.sndarray.array([]))
    score_sound = pygame.mixer.Sound(pygame.sndarray.array([]))


class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = 8

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        pygame.draw.rect(screen, PADDLE_COLOR, (self.x, self.y, self.width, self.height))
        # Add a shine effect to the paddle
        pygame.draw.rect(screen, (200, 230, 255), (self.x, self.y, self.width, 4))


class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.dx = random.choice([-4, -3, 3, 4])
        self.dy = -4

    def move(self, paddle, bricks):
        self.x += self.dx
        self.y += self.dy

        # Wall collisions
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
            pong_sound.play()

        if self.y <= self.radius:
            self.dy *= -1
            pong_sound.play()

        # Paddle collision
        if (self.y + self.radius >= paddle.y and
                self.x >= paddle.x and
                self.x <= paddle.x + paddle.width and
                self.y < paddle.y + paddle.height):
            # Adjust bounce angle based on where the ball hits the paddle
            paddle_center = paddle.x + paddle.width / 2
            distance_from_center = self.x - paddle_center
            self.dx = distance_from_center * 0.1
            self.dy *= -1
            pong_sound.play()

        # Brick collisions
        brick_hit = False
        for brick in bricks:
            if brick.active:
                if (self.x + self.radius >= brick.x and
                        self.x - self.radius <= brick.x + BRICK_WIDTH and
                        self.y + self.radius >= brick.y and
                        self.y - self.radius <= brick.y + BRICK_HEIGHT):
                    brick.active = False
                    self.dy *= -1
                    score_sound.play()
                    brick_hit = True

        # Bottom screen collision (lose a life)
        if self.y >= HEIGHT:
            return "miss"

        return brick_hit

    def draw(self):
        pygame.draw.circle(screen, BALL_COLOR, (int(self.x), int(self.y)), self.radius)
        # Add a shine effect to the ball
        pygame.draw.circle(screen, (230, 230, 230), (int(self.x - 3), int(self.y - 3)), 3)


class Brick:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.active = True

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT))
            # Add a border to the brick
            pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, BRICK_WIDTH, BRICK_HEIGHT), 2)


# Create game objects
paddle = Paddle()
ball = Ball()

# Create bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
        brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
        color = BRICK_COLORS[row % len(BRICK_COLORS)]
        bricks.append(Brick(brick_x, brick_y, color))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state != "playing":
                if game_state == "game_over" or game_state == "win":
                    # Reset game
                    score = 0
                    lives = 3
                    level = 1
                    bricks = []
                    for row in range(BRICK_ROWS):
                        for col in range(BRICK_COLS):
                            brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
                            brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
                            color = BRICK_COLORS[row % len(BRICK_COLORS)]
                            bricks.append(Brick(brick_x, brick_y, color))
                    ball.reset()
                    paddle = Paddle()
                game_state = "playing"

    # Get keyboard input for paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move("left")
    if keys[pygame.K_RIGHT]:
        paddle.move("right")

    # Fill the screen with background color
    screen.fill(BACKGROUND)

    # Draw the game elements
    paddle.draw()
    ball.draw()

    # Draw bricks and check if all are destroyed
    active_bricks = 0
    for brick in bricks:
        brick.draw()
        if brick.active:
            active_bricks += 1

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    level_text = font.render(f"Level: {level}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))
    screen.blit(level_text, (WIDTH // 2 - 50, 10))

    # Game logic
    if game_state == "playing":
        # Move the ball and check for collisions
        result = ball.move(paddle, bricks)
        if result == "miss":
            lives -= 1
            if lives <= 0:
                game_state = "game_over"
            else:
                ball.reset()
        elif result:
            score += 10

        # Check if all bricks are destroyed
        if active_bricks == 0:
            level += 1
            ball.reset()
            # Create new bricks for the next level
            bricks = []
            for row in range(BRICK_ROWS + level - 1):
                for col in range(BRICK_COLS):
                    brick_x = col * (BRICK_WIDTH + BRICK_GAP) + BRICK_GAP
                    brick_y = row * (BRICK_HEIGHT + BRICK_GAP) + BRICK_GAP + 50
                    color = BRICK_COLORS[row % len(BRICK_COLORS)]
                    bricks.append(Brick(brick_x, brick_y, color))

            # Increase ball speed for higher levels
            ball.dx *= 1.1
            ball.dy *= 1.1

            # Check for win condition (after level 5)
            if level > 5:
                game_state = "win"

    # Display game messages
    if game_state == "start":
        title_text = font.render("BREAKOUT", True, (255, 215, 0))
        start_text = font.render("Press SPACE to Start", True, TEXT_COLOR)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 20))

    elif game_state == "game_over":
        over_text = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press SPACE to Restart", True, TEXT_COLOR)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    elif game_state == "win":
        win_text = font.render("YOU WIN!", True, (0, 255, 0))
        final_score = font.render(f"Final Score: {score}", True, TEXT_COLOR)
        restart_text = font.render("Press SPACE to Play Again", True, TEXT_COLOR)
        screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 40))

    # Draw a border around the play area
    pygame.draw.rect(screen, (60, 60, 100), (0, 0, WIDTH, HEIGHT), 10)

    # Update the display
    pygame.display.flip()

    # Control the game speed
    clock.tick(60)

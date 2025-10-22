import pyautogui
import time
import webbrowser
from PIL import ImageGrab

GAME_URL = "https://elgoog.im/t-rex/"
GAME_AREA = (100, 300, 800, 500)  # More reasonable default area
OBSTACLE_THRESHOLD = 150  # Sum of RGB values to consider as obstacle
SLEEP_TIME = 0.05
PIXEL_STEP = 3
JUMP_COOLDOWN = 10  # Prevents multiple jumps for same obstacle
cooldown_counter = 0


def detect_obstacle():
    """Detects if there is an obstacle in the defined game area."""
    global cooldown_counter

    if cooldown_counter > 0:
        cooldown_counter -= 1
        return False

    try:
        # Capture screen
        screen = ImageGrab.grab(bbox=GAME_AREA)
        width, height = screen.size

        # Check multiple points ahead of the dino
        check_points = [
            (int(width * 0.6), int(height * 0.7)),  # Main obstacle detection
            (int(width * 0.55), int(height * 0.6)),  # For birds
            (int(width * 0.5), int(height * 0.7))  # Earlier detection
        ]

        for x, y in check_points:
            if x < width and y < height:  # Ensure within bounds
                r, g, b = screen.getpixel((x, y))
                # Check if pixel is dark (obstacle)
                if (r + g + b) < OBSTACLE_THRESHOLD:
                    cooldown_counter = JUMP_COOLDOWN
                    return True

        return False
    except Exception as e:
        print(f"Error detecting obstacle: {e}")
        return False


def detect_game_over():
    """Check if the game has ended by looking for the restart button."""
    try:
        screen = ImageGrab.grab(bbox=GAME_AREA)
        width, height = screen.size

        # Look for the bright restart button
        restart_area = (int(width * 0.5), int(height * 0.6),
                        int(width * 0.7), int(height * 0.8))

        for x in range(restart_area[0], restart_area[2], PIXEL_STEP):
            for y in range(restart_area[1], restart_area[3], PIXEL_STEP):
                r, g, b = screen.getpixel((x, y))
                if (r + g + b) > 500:  # Very bright pixels = restart button
                    return True
        return False
    except Exception as e:
        print(f"Error detecting game over: {e}")
        return False


def jump():
    """Simulates a jump by pressing the space bar."""
    pyautogui.press('space')


def open_game():
    """Opens the T-Rex game in the default web browser."""
    print("Opening the T-Rex game...")
    webbrowser.open(GAME_URL)
    time.sleep(3)
    print("Please make sure the game is visible on screen")
    print("Press 'Q' to quit the bot")


def play_game():
    """Main loop to run the T-Rex game."""
    print("Starting the T-Rex game automation...")
    time.sleep(2)

    # Start the game
    jump()
    time.sleep(1)

    while True:
        # Check for quit command
        if pyautogui.keyIsPressed('q'):
            print("Quitting...")
            break

        # Check if game over and restart
        if detect_game_over():
            print("Game over detected. Restarting...")
            jump()
            time.sleep(1)
            continue

        # Check for obstacles and jump
        if detect_obstacle():
            print("Obstacle detected! Jumping...")
            jump()

        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    try:
        open_game()
        play_game()
    except KeyboardInterrupt:
        print("Game automation stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

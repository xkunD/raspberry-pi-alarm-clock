import pygame
import random
import os
import RPi.GPIO as GPIO
# Setup GPIO for shutdown functionality
run_flag = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_callback(channel):
    global run_flag
    run_flag = False

GPIO.add_event_detect(17, GPIO.FALLING, callback=quit_callback, bouncetime=300)
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use the piTFT frame buffer
os.putenv('SDL_FBDEV', '/dev/fb1')  # Specify the piTFT device

# Initialize pygame
pygame.init()

# Configure screen resolution (e.g., 800x600 for a desktop monitor)
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snowy Scenario")

# Load the snowflake image
snowflake_image = pygame.image.load("snow.png").convert_alpha()  # Ensure transparency

# Resize the image if necessary
snowflake_image = pygame.transform.scale(snowflake_image, (20, 20))  # Adjust size if needed

# Snowflake properties
NUM_SNOWFLAKES = 100
snowflakes = [{"x": random.randint(0, SCREEN_WIDTH), 
               "y": random.randint(-SCREEN_HEIGHT, SCREEN_HEIGHT),
               "speed": random.randint(1, 3)} for _ in range(NUM_SNOWFLAKES)]

# Set up the clock for a smooth frame rate
clock = pygame.time.Clock()


while run_flag:
    # Clear the screen
    screen.fill((0, 0, 0))  # Black background

    # Draw snowflakes
    for flake in snowflakes:
        screen.blit(snowflake_image, (flake["x"], flake["y"]))
        flake["y"] += flake["speed"]

        # Reset snowflake to the top if it goes off the screen
        if flake["y"] > SCREEN_HEIGHT:
            flake["y"] = random.randint(-20, -1)
            flake["x"] = random.randint(0, SCREEN_WIDTH)

    # Update the display
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow ESC key to exit
                running = False

    # Cap the frame rate
    clock.tick(30)

pygame.quit()

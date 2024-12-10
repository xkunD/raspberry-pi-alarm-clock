import pygame  # Import pygame graphics library
import os  # For OS calls
import time  # For time handling
import RPi.GPIO as GPIO
import random

# Setup GPIO for shutdown functionality
run_flag = True
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_callback(channel):
    global run_flag
    run_flag = False

GPIO.add_event_detect(17, GPIO.FALLING, callback=quit_callback, bouncetime=300)

# Setup piTFT display
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use the piTFT frame buffer
os.putenv('SDL_FBDEV', '/dev/fb1')  # Specify the piTFT device

# Initialize pygame
pygame.init()
pygame.mouse.set_visible(False)

# Set up display
size = width, height = 320, 240  # Screen resolution for piTFT
screen = pygame.display.set_mode(size)
black = 0, 0, 0
white = 255, 255, 255
font = pygame.font.Font(None, 40)  # Font size 40
font1 = pygame.font.Font(None, 60)  # Font size 60

# Clock for updating
myclock = pygame.time.Clock()
FPS = 30  # Smooth snowflake animation

# Load the snowflake image
snowflake_image = pygame.image.load("snow.png").convert_alpha()  # Ensure transparency
snowflake_image = pygame.transform.scale(snowflake_image, (20, 20))  # Adjust size if needed

# Snowflake properties
NUM_SNOWFLAKES = 100
snowflakes = [{"x": random.randint(0, width), 
               "y": random.randint(-height, height),
               "speed": random.randint(1, 3)} for _ in range(NUM_SNOWFLAKES)]

# Math problem generator
def problem_generator():
    num1 = random.randint(100, 500)
    num2 = random.randint(50, 100)
    if random.randint(1, 2) == 1:
        operation = "+"
    else:
        operation = "-"
    return f"{num1} {operation} {num2} = ?"

math_problem = problem_generator()
last_problem_time = time.time()

# Main loop
while run_flag:
    myclock.tick(FPS)

    # Get the current time
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Update math problem every 10 seconds
    if time.time() - last_problem_time >= 10:
        math_problem = problem_generator()
        last_problem_time = time.time()

    # Clear the screen
    screen.fill(black)

    # Draw snowflakes
    for flake in snowflakes:
        screen.blit(snowflake_image, (flake["x"], flake["y"]))
        flake["y"] += flake["speed"]

        # Reset snowflake to the top if it goes off the screen
        if flake["y"] > height:
            flake["y"] = random.randint(-20, -1)
            flake["x"] = random.randint(0, width)

    # Create a semi-transparent overlay for text
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Black with 50% transparency
    screen.blit(overlay, (0, 0))

    # Render and display the time
    time_surface = font.render(current_time, True, white)
    time_rect = time_surface.get_rect(center=(width - 80, 20))
    screen.blit(time_surface, time_rect)

    # Render and display the math problem
    math_surface = font1.render(math_problem, True, (200, 150, 200))
    math_rect = math_surface.get_rect(center=(width // 2, height // 2))
    screen.blit(math_surface, math_rect)

    # Update the display
    pygame.display.flip()

# Cleanup
pygame.quit()
GPIO.cleanup()

import pygame
import random
import os
import RPi.GPIO as GPIO
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
# Configure screen resolution (e.g., 320x240 for PiTFT or 800x600 for desktop)
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rainy Scenario")

# Load the raindrop image
raindrop_image = pygame.image.load("rain.png").convert_alpha()  # Ensure transparency

# Resize the image if necessary
raindrop_image = pygame.transform.scale(raindrop_image, (10, 20))  # Adjust size as needed

# Raindrop properties
NUM_RAINDROPS = 100
raindrops = [{"x": random.randint(0, SCREEN_WIDTH), 
              "y": random.randint(-SCREEN_HEIGHT, 0),
              "speed": random.randint(5, 10)} for _ in range(NUM_RAINDROPS)]

# Set up the clock for a smooth frame rate
clock = pygame.time.Clock()
FPS = 30

running = True
while run_flag:
    # Clear the screen (set to a dark blue for a rainy effect)
    screen.fill((0, 0, 0))

    # Draw raindrops
    for drop in raindrops:
        screen.blit(raindrop_image, (drop["x"], drop["y"]))
        drop["y"] += drop["speed"]

        # Reset raindrop to the top if it goes off the screen
        if drop["y"] > SCREEN_HEIGHT:
            drop["y"] = random.randint(-20, 0)
            drop["x"] = random.randint(0, SCREEN_WIDTH)

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
    clock.tick(FPS)

pygame.quit()

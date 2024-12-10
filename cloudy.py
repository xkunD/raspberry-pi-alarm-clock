import pygame
import os

# Initialize pygame
pygame.init()

# Configure screen resolution for PiTFT
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cloud Display")

# Load the cloud image
cloud_image = pygame.image.load("cloudy.png").convert_alpha()  # Ensure transparency

# Resize the cloud image if necessary
cloud_image = pygame.transform.scale(cloud_image, (125, 80))  # Cloud spans the top

# Main loop
running = True
while running:
    # Clear the screen (black background)
    screen.fill((0, 0, 0))  # Black background

    # Draw the cloud at the top
    screen.blit(cloud_image, (0, 0))
    screen.blit(cloud_image, (120, 0))

    # Update the display
    pygame.display.flip()

    # Event handling to exit the program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Allow ESC key to exit
                running = False

# Cleanup
pygame.quit()

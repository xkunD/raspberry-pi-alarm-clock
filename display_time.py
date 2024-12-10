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
font = pygame.font.Font(None, 40)  # Font size 50
font1 = pygame.font.Font(None, 60)
# Clock for updating
myclock = pygame.time.Clock()
FPS = 1  # Update once per second
def problem_generator():
	num1 = random.randint(100,500)
	num2 = random.randint(50,100)
	num3 = random.randint(1,2)
	if num3 ==1:
		type = "+"
	else:
		type = "-"
	problem = f" {num1} {type} {num2} = ?"
	return problem

math_problem = problem_generator()
last_problem_time = time.time()
while run_flag:
    myclock.tick(FPS)
    
    # Get the current time
    current_time = time.strftime("%H:%M:%S", time.localtime())
    
    
    #counter for the math problem 
    if time.time() - last_problem_time >= 10:
        math_problem = problem_generator()
        last_problem_time = time.time()
    
    # Render the time as text
    time_surface = font.render(current_time, True, white)
    time_rect = time_surface.get_rect(center=(width-80, 10))   #width/2, height/2
    
    #Initialization for math problems
    math_surface = font1.render(math_problem, True, (200,150,200))
    math_rect = math_surface.get_rect()
    math_rect.center = (width //2, height // 2)
    
    # Clear the screen
    screen.fill(black)
    
    # Display the time
    screen.blit(time_surface, time_rect)
    screen.blit(math_surface, math_rect)
    pygame.display.flip()  # Update the display

# Cleanup
pygame.quit()
GPIO.cleanup()

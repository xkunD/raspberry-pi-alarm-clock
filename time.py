#time.py
import pygame,pigame
import os
import time
import RPi.GPIO as GPIO
import random
import requests
import time
from datetime import datetime
from filelock import FileLock
from ai_test import test_openai_assistant

# GPIO setup for shutdown
run_flag = True
math_flag = False
ai_flag = False
print_flag10 = True
print_flag15 = True
run_times = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_callback(channel):
    global run_flag
    run_flag = False
    math_flag = False
    ai_flag = False


GPIO.add_event_detect(17, GPIO.FALLING, callback=quit_callback, bouncetime=300)

# Setup piTFT display
#os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use the piTFT frame buffer
#os.putenv('SDL_FBDEV', '/dev/fb1')  # Specify the piTFT device
#os.putenv('SDL_MOUSEDRV','dummy')
#os.putenv('SDL_MOUSEDEV','/dev/null')
#os.putenv('DISPLAY','')

# Initialize pygame
pygame.init()
pygame.mouse.set_visible(True)
pitft = pigame.PiTft()
#Alarm communication
alarm_trigger_file = "alarm_trigger.txt"

def trigger_alarm():
    with open(alarm_trigger_file, "w") as f:
        f.write("RING")

# Clear the alarm trigger file
def clear_alarm_trigger():
    with open(alarm_trigger_file, "w") as f:
        f.write("")

# Set up display
size = width, height = 320, 240  # Screen resolution for piTFT
screen = pygame.display.set_mode(size)
black = 0, 0, 0
white = 255, 255, 255
font = pygame.font.Font(None, 30)
font_large = pygame.font.Font(None, 60)
font1 = pygame.font.Font(None, 60)
# Alarm variables
alarm_time = None
alarm_screen = False
alarm_hours = 0
alarm_minutes = 0

# Button dimensions
button_width = 80
button_height = 40
button_color = (100, 100, 200)
button_highlight = (200, 200, 255)

output_file = "voice_output.txt"
trigger_file = "trigger.txt"
output_file_ai = "output_file_ai.txt"
lock_output = FileLock(f"{output_file}.lock")
lock_trigger = FileLock(f"{trigger_file}.lock")
with open(output_file, "w") as f:
                f.write('')
with open(trigger_file, "w") as f:
                f.write('')
#math problem 
def problem_generator():
	num1 = random.randint(100,500)
	num2 = random.randint(50,100)
	num3 = random.randint(1,2)
	if num3 ==1:
		type = "+"
	else:
		type = "-"
	problem = f" {num1} {type} {num2} = ?"
	return f"{num1} {type} {num2} = ?", eval(f"{num1} {type} {num2}")

math_problem, correct_answer = problem_generator()


#get weather information
def get_weather(api_key, city):
    # OpenWeather API endpoint for current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    current_weather = ''
    try:
        # Make the HTTP request
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        weather_data = response.json()
        rain_weather = ['rain','shower rain', 'thunderstorm', 'light rain', 'moderate rain', 'heavy intensity rain']
        snow_weather = ['snow']
        cloudy_weather = ['mist', 'broken clouds', 'scattered clouds', 'few clouds', 'overcast clouds']
        #Extract the weather description (e.g., sunny, cloudy, rain)
        weather_description = weather_data['weather'][0]['description']
        if weather_description in cloudy_weather:
            print(weather_description, 'is cloudy')
            current_weather = 'cloudy'
        elif weather_description in rain_weather:
            print(weather_description, 'is rain')
            current_weather = 'rainy'
        else:
            current_weather = weather_description
        return current_weather
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

API_KEY = "b0daa1d2a19d02135aea6e6dafee4415"  # Replace with your OpenWeather API key
CITY = "Fukuoka"  # Replace with your city
weather = get_weather(API_KEY, CITY)
# Clock
myclock = pygame.time.Clock()
FPS = 30

def draw_button(text, x, y, highlight=False):
    color = button_highlight if highlight else button_color
    pygame.draw.rect(screen, color, (x, y, button_width, button_height))
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
    screen.blit(text_surface, text_rect)

# Main loop
while True:  # Keep the program running
    while run_flag:  # Main clock loop
        pitft.update()
        myclock.tick(FPS)
        screen.fill(black)
        current_time = time.strftime("%H:%M:%S", time.localtime())

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_flag = False
                math_flag = False  # End the program completely
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                print("coordinate::",x, y)
                if alarm_screen:
                    # Handle up and down buttons
                    if 50 <= x <= 50 + button_width:
                        if 50 <= y <= 50 + button_height:  # Up hour
                            alarm_hours = (alarm_hours + 1) % 24
                        elif 150 <= y <= 150 + button_height:  # Down hour
                            alarm_hours = (alarm_hours - 1) % 24
                    elif 200 <= x <= 200 + button_width:
                        if 50 <= y <= 50 + button_height:  # Up minute
                            alarm_minutes = (alarm_minutes + 1) % 60
                        elif 150 <= y <= 150 + button_height:  # Down minute
                            alarm_minutes = (alarm_minutes - 1) % 60
                    # Handle confirm button
                    if 100 <= x <= 220 and 200 <= y <= 250:
                        alarm_time = f"{alarm_hours:02}:{alarm_minutes:02}:00"
                        now = datetime.now()
                        alarm_timestamp = datetime(now.year, now.month, now.day, alarm_hours, alarm_minutes).timestamp()
                        alarm_screen = False
                else:
                    # Check if "Set Alarm" button is pressed
                    if 40 <= x <= 120 and 180 <= y <= 240:
                        alarm_screen = True
                    if 160 <= x <= 240 and 180 <= y <= 240:
                        print("click ai")
                        ai_flag = True
                        run_flag = False

        # Alarm screen
        if alarm_screen:
            # Display alarm setting interface
            alarm_display = f"Alarm: {alarm_hours:02}:{alarm_minutes:02}"
            alarm_surface = font_large.render(alarm_display, True, white)
            alarm_rect = alarm_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(alarm_surface, alarm_rect)

            # Draw buttons
            draw_button("Hour +", 50, 50)
            draw_button("Hour -", 50, 150)
            draw_button("Min +", 200, 50)
            draw_button("Min -", 200, 150)
            draw_button("Confirm", 100, 200)
        else:
            # Display current time
            time_surface = font_large.render(current_time, True, white)
            time_rect = time_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(time_surface, time_rect)

            # Draw "Set Alarm" button
            draw_button("Set Alarm", 60, 200)
            draw_button("AI", 180, 200)
        # Check alarm
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if alarm_time and current_time == alarm_time:
            trigger_alarm()
            time.sleep(10)
            clear_alarm_trigger()
            last_problem_time = time.time()
            math_flag = True
            run_flag = False  # Pause the clock loop to enter math mode

        pygame.display.flip()

    counter = 0
    correct = 0
    NUM_SNOWFLAKES = 100
    snowflake_image = pygame.image.load("snow.png").convert_alpha()
    snowflake_image = pygame.transform.scale(snowflake_image, (20, 20))
    #snowflake_image.fill((255, 255, 255))  # White color
    snowflakes = [{"x": random.randint(0, width), "y": random.randint(-height, height), "speed": random.randint(1, 3)} for _ in range(NUM_SNOWFLAKES)]
    # Load the cloud image
    cloud_image = pygame.image.load("cloudy.png").convert_alpha()  # Ensure transparency
    # Load the raindrop image
    raindrop_image = pygame.image.load("rain.png").convert_alpha()  # Ensure transparency

    # Resize the image if necessary
    raindrop_image = pygame.transform.scale(raindrop_image, (10, 20))  # Adjust size as needed

# Raindrop properties
    NUM_RAINDROPS = 100
    raindrops = [{"x": random.randint(0, width), 
                  "y": random.randint(-height, 0),
                  "speed": random.randint(5, 10)} for _ in range(NUM_RAINDROPS)]
# Resize the cloud image if necessary
    cloud_image = pygame.transform.scale(cloud_image, (125, 80))  # Cloud spans the top
    feedback_message = ""  # Variable to store feedback message
    feedback_timer = 0     # Timer to control feedback visibility
    while ai_flag:
        screen.fill(black)
        pygame.display.flip()  # Update the display
        with open(output_file_ai, "w") as f:
                f.write('')
        with lock_trigger:
            with open(trigger_file, "w") as f:
                f.write("START")
                print("should written start")
        try:
            with open(output_file_ai, "r") as f:
                time.sleep(10)
                voice_input = f.read().strip()
                print(voice_input)
                reply = test_openai_assistant(voice_input)
            draw_button(reply,50,50)
            pygame.display.flip()  # Update the display
            with lock_trigger:
                with open(trigger_file, "w") as f:
                    f.write("STOP")
            time.sleep(15)
            ai_flag = False
            run_flag = True
        except FileNotFoundError:
                pass  # File not yet created, continue loop

    while math_flag:  # Math question loop
        myclock.tick(FPS)
        current_time = time.strftime("%H:%M:%S", time.localtime())
        if time.time() - last_problem_time >= 20:
            math_problem, correct_answer = problem_generator()
            print_flag10 = True
            print_flag15 = True
            with open(output_file, "w") as f:
                f.write('')
            counter += 1
            last_problem_time = time.time()
            feedback_message = ""  # Clear feedback message
    # Clear the screen and draw the snowflakes
        screen.fill(black)
        if (weather == "snow"):
            for flake in snowflakes:
                screen.blit(snowflake_image, (flake["x"], flake["y"]))
                flake["y"] += flake["speed"]  # Move the snowflake down

        # Reset snowflake to the top if it goes off the screen
                if flake["y"] > height:
                    flake["y"] = random.randint(-20, -1)
                    flake["x"] = random.randint(0, width)
        elif (weather == "cloudy"):
            screen.blit(cloud_image, (0, 0))
            screen.blit(cloud_image, (120, 0))
        elif (weather == "rainy"):
            for drop in raindrops:
                screen.blit(raindrop_image, (drop["x"], drop["y"]))
                drop["y"] += drop["speed"]

        # Reset raindrop to the top if it goes off the screen
                if drop["y"] > height:
                    drop["y"] = random.randint(-20, 0)
                    drop["x"] = random.randint(0, width)

    # Render the current time
        time_surface = font.render(current_time, True, white)
        time_rect = time_surface.get_rect(center=(width - 80, 10))

    # Render the math problem
        math_surface = font1.render(math_problem, True, (200, 150, 200))
        math_rect = math_surface.get_rect(center=(width // 2, height // 2))

    # Display the time and math problem on top of the snowflake background
        screen.blit(time_surface, time_rect)
        screen.blit(math_surface, math_rect)
        with lock_trigger:
            with open(trigger_file, "w") as f:
                f.write("START")
        pygame.display.flip()  # Update the display
        try:
                # Read voice input from file
            with open(output_file, "r") as f:
                voice_input = f.read().strip()

                # Process voice input
            if (time.time() - last_problem_time >= 10) and print_flag10:
                if voice_input:
                    voice_input = ''.join(filter(str.isdigit, voice_input))
                    print("Voice input received at 10s of counter:", counter, 'with content:' ,voice_input)
                    if voice_input.isdigit() and int(voice_input) == correct_answer:
                        print("Correct answer!")
                        feedback_message = "Correct answer!"
                        correct += 1
                        print_flag10 = False
                        print_flag15 = False
                    else:
                        print("Incorrect. Try again.")
                        feedback_message = "Incorrect. Try again."
                        print_flag10 = False
                    
                else:
                    print("no content at 10s of counter:", counter)
                    print_flag10 = False
                    feedback_message = "No input received. Try again."
                if feedback_message:
                    feedback_surface = font.render(feedback_message, True, white)
                    feedback_rect = feedback_surface.get_rect(center=(width // 2, (height // 2) + 40))
                    screen.blit(feedback_surface, feedback_rect)
                    pygame.display.flip()
                    time.sleep(1)

                    #if voice_input.isdigit() and int(voice_input) == correct_answer:
                    #    print("Correct answer!")
                    #    counter += 1
                    #    math_problem, correct_answer = problem_generator()
                    #else:
                    #    print("Incorrect. Try again.")
            if (time.time() - last_problem_time >= 19) and print_flag15:
                feedback_message = ""  # Clear feedback message
                alarm_on_15 = False
                if voice_input:
                    print_flag15 = False
                    print("Voice input received at 15s of counter:", counter, 'with content:', voice_input)
                    if voice_input.isdigit() and int(voice_input) == correct_answer:
                        print("Correct answer!")
                        feedback_message = "Correct answer!"
                        correct += 1
                    else:
                        print("Incorrect. One more question added.")
                        feedback_message = "Incorrect. One more question"
                        run_times += 1
                        last_problem_time += 5
                        alarm_on_15 = True
                else:
                    print("no content at 15s of counter:", counter, "One more question added.")
                    feedback_message = "No input received. One more question."
                    print_flag15 = False
                    run_times += 1
                    last_problem_time += 5
                    alarm_on_15 = True
                if feedback_message:
                    feedback_surface = font.render(feedback_message, True, white)
                    feedback_rect = feedback_surface.get_rect(center=(width // 2, (height // 2) + 40))
                    screen.blit(feedback_surface, feedback_rect)
                    pygame.display.flip()
                    time.sleep(1)
                if alarm_on_15:
                    trigger_alarm()
                    time.sleep(5)
                    clear_alarm_trigger()

        except FileNotFoundError:
                pass  # File not yet created, continue loop
        if correct == 4:
            math_flag = False
            with lock_trigger:
                with open(trigger_file, "w") as f:
                    f.write("STOP")
            run_flag = True  # Resume the main clock loop
    if not (run_flag or math_flag):
        break


# Cleanup
del(pitft)
pygame.quit()
GPIO.cleanup()
import requests

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
        rain_weather = ['rain','shower rain', 'thunderstorm']
        snow_weather = ['snow']
        cloudy_weather = ['mist', 'broken clouds', 'scattered clouds', 'few clouds']
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
        return weather_description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Example usage
if __name__ == "__main__":
    API_KEY = "b0daa1d2a19d02135aea6e6dafee4415"  # Replace with your OpenWeather API key
    CITY = "Ithaca"  # Replace with your city
    
    weather = get_weather(API_KEY, CITY)
    if weather:
        print(f"The current weather in {CITY} is: {weather}")
        
        
        
import pygame
import os
import time
import RPi.GPIO as GPIO
import random
from filelock import FileLock

# GPIO setup
run_flag = True
math_flag = False
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_callback(channel):
    global run_flag
    run_flag = False
    math_flag = False

GPIO.add_event_detect(17, GPIO.FALLING, callback=quit_callback, bouncetime=300)

# Initialize pygame
pygame.init()
pygame.mouse.set_visible(True)

# Set up display
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
black = 0, 0, 0
white = 255, 255, 255
font = pygame.font.Font(None, 30)
font1 = pygame.font.Font(None, 60)

# Files for communication
output_file = "voice_output.txt"
trigger_file = "trigger.txt"
lock_output = FileLock(f"{output_file}.lock")
lock_trigger = FileLock(f"{trigger_file}.lock")

# Clock and FPS
myclock = pygame.time.Clock()
FPS = 30

# Math problem generator
def problem_generator():
    num1 = random.randint(100, 500)
    num2 = random.randint(50, 100)
    operator = "+" if random.randint(1, 2) == 1 else "-"
    return f"{num1} {operator} {num2} = ?", eval(f"{num1} {operator} {num2}")

# Main loop
while True:
    while run_flag:
        # Display clock
        myclock.tick(FPS)
        screen.fill(black)
        current_time = time.strftime("%H:%M:%S", time.localtime())

        # Draw current time
        time_surface = font1.render(current_time, True, white)
        time_rect = time_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(time_surface, time_rect)
        pygame.display.flip()

        # Simulate alarm condition
        if math_flag:  # Enter math question loop
            break

    # Math question loop
    if math_flag:
        math_problem, correct_answer = problem_generator()

        # Trigger the voice.py to start listening
        with lock_trigger:
            with open(trigger_file, "w") as f:
                f.write("START")

        counter = 0

        while counter < 6:
            myclock.tick(FPS)
            screen.fill(black)

            # Draw math problem
            math_surface = font1.render(math_problem, True, white)
            math_rect = math_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(math_surface, math_rect)
            pygame.display.flip()

            try:
                # Read voice input from file
                with lock_output:
                    with open(output_file, "r") as f:
                        voice_input = f.read().strip()

                # Process voice input
                if voice_input:
                    print("Voice input received:", voice_input)
                    if voice_input.isdigit() and int(voice_input) == correct_answer:
                        print("Correct answer!")
                        counter += 1
                        math_problem, correct_answer = problem_generator()
                    else:
                        print("Incorrect. Try again.")
            except FileNotFoundError:
                pass  # File not yet created, continue loop

        # Stop voice.py from listening
        with lock_trigger:
            with open(trigger_file, "w") as f:
                f.write("STOP")

        math_flag = False
        run_flag = True

pygame.quit()
GPIO.cleanup(
)




import speech_recognition as sr
from filelock import FileLock
import time

# Initialize recognizer
r = sr.Recognizer()
mic = sr.Microphone()

# Files for communication
output_file = "voice_output.txt"
trigger_file = "trigger.txt"
lock_output = FileLock(f"{output_file}.lock")
lock_trigger = FileLock(f"{trigger_file}.lock")

print("Voice recognition ready.")

while True:
    try:
        # Check trigger file
        with lock_trigger:
            with open(trigger_file, "r") as f:
                trigger = f.read().strip()

        if trigger == "START":
            print("Listening for voice input...")
            with mic as source:
                r.adjust_for_ambient_noise(source)
                print("Say something...")
                audio = r.listen(source)

            # Recognize speech
            try:
                words = r.recognize_google(audio, language="en-US")
                print("Recognized:", words)

                # Write recognized speech to output file
                with lock_output:
                    with open(output_file, "w") as f:
                        f.write(words)
            except sr.UnknownValueError:
                print("Could not understand the audio.")
            except sr.RequestError as e:
                print(f"Request error: {e}")
        else:
            # Wait briefly before rechecking the trigger
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting voice recognition.")
        break


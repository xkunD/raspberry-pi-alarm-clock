# Helper functions for weather animations
def update_snowflakes(snowflakes, snowflake_image, width, height):
    for flake in snowflakes:
        screen.blit(snowflake_image, (flake["x"], flake["y"]))
        flake["y"] += flake["speed"]
        if flake["y"] > height:
            flake["y"] = random.randint(-20, -1)
            flake["x"] = random.randint(0, width)

def update_raindrops(raindrops, raindrop_image, width, height):
    for drop in raindrops:
        screen.blit(raindrop_image, (drop["x"], drop["y"]))
        drop["y"] += drop["speed"]
        if drop["y"] > height:
            drop["y"] = random.randint(-20, 0)
            drop["x"] = random.randint(0, width)

def update_clouds(cloud_image, width):
    screen.blit(cloud_image, (0, 0))
    screen.blit(cloud_image, (width // 2, 0))

def display_weather_animation(weather):
    if weather == "snow":
        update_snowflakes(snowflakes, snowflake_image, width, height)
    elif weather == "rainy":
        update_raindrops(raindrops, raindrop_image, width, height)
    elif weather == "cloudy":
        update_clouds(cloud_image, width)

# Refactored math_flag loop
counter = 0
while math_flag:
    myclock.tick(FPS)
    current_time = time.strftime("%H:%M:%S", time.localtime())

    # Generate a new math problem every 10 seconds
    if time.time() - last_problem_time >= 10:
        math_problem = problem_generator()
        counter += 1
        last_problem_time = time.time()

    # Clear the screen and display weather animation
    screen.fill(black)
    display_weather_animation(weather)

    # Render the current time
    time_surface = font.render(current_time, True, white)
    time_rect = time_surface.get_rect(center=(width - 80, 10))

    # Render the math problem
    math_surface = font1.render(math_problem, True, (200, 150, 200))
    math_rect = math_surface.get_rect(center=(width // 2, height // 2))

    # Display the time and math problem
    screen.blit(time_surface, time_rect)
    screen.blit(math_surface, math_rect)
    pygame.display.flip()  # Update the display

    # End math mode after 6 questions
    if counter == 6:
        math_flag = False
        run_flag = True  # Resume the main clock loop

import pygame
import time
import math


# Some config width height settings
canvas_width = 640
canvas_height = 480

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
# Set the window title
pygame.display.set_caption("Sine Wave")

# Make a screen to see
screen = pygame.display.set_mode((canvas_width, canvas_height))
screen.fill(background_color)

# Make a surface to draw on
surface = pygame.Surface((canvas_width, canvas_height))
surface.fill(background_color)


# Simple main loop
frequency = 5
amplitude = 50
speed = 1
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                frequency -= 1
            if event.key == pygame.K_RIGHT:
                frequency += 1
            if event.key == pygame.K_UP:
                amplitude -= 1
            if event.key == pygame.K_DOWN:
                amplitude += 1
            if event.key == pygame.K_a:
                speed -= 1
            if event.key == pygame.K_s:
                speed += 1

    # Redraw the background
    surface.fill(background_color)


    # Update sine wave
    for x in range(0, canvas_width):
        y = int((canvas_height/2) + amplitude*math.sin(frequency*((float(x)/canvas_width)*(2*math.pi) + (speed*time.time()))))
        surface.set_at((x, y), color)

    # Put the surface we draw on, onto the screen
    screen.blit(surface, (0, 0))

    # Show it.
    pygame.display.flip()

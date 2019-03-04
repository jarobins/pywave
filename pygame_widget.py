import pygame, sys
import numpy as np
import math
import time
import random
from pygame.locals import *

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 24)

class SignalWindow():
    def __init__(self, surface, pos, color=(255,255,255)):
        self.font    = pygame.font.SysFont('monospace', 18)
        self.surface = surface
        self.pos     = pos
        self.width   = 400
        self.height  = 200
        self.rect    = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.active  = 0
        self.color   = color

    def draw(self, pointlist):
        ''' Draw to button'''
        pygame.draw.rect(self.surface, [255, 255, 255], self.rect, 2)  # draw button
        pygame.draw.line(self.surface, [255,255,0],
                         (self.pos[0], self.pos[1]+(self.height/2)),
                         (self.pos[0]+self.width, self.pos[1]+self.height/2))
        pygame.draw.lines(self.surface, self.color, 0,
                          [(self.pos[0]+x, self.pos[1]-y+100) for x, y in pointlist])


class GameButton():
    def __init__(self, label, surface, pos, width=100, height=40):
        self.font = pygame.font.SysFont('monospace', 18)
        self.label = self.font.render('%s' % label, False, (255, 255, 255))
        self.surface = surface
        self.pos = pos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.active = 0

    def draw(self):
        ''' Draw to button'''
        pygame.draw.rect(self.surface, [255, 255, 255], self.rect, 2)  # draw button
        self.surface.blit(self.label,(self.pos[0]+10,self.pos[1]+10))

    def selected(self, pos):
        """ Change the color of the button"""
        if pos:
            self.color    = (255, 255, 255)
            self.active = 1
        else:
            self.color    = (180, 180, 180)
            self.active = 0


class MixerButton():
    def __init__(self, label, surface, pos):
        self.color = (255, 255, 255)
        self.font = pygame.font.SysFont('monospace', 18)
        self.label = self.font.render('%s' % label, False, (255, 255, 255))
        self.surface = surface
        self.pos = pos
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.active = 0

    def draw(self):
        ''' Draw to button'''
        pygame.draw.ellipse(self.surface, self.color, self.rect, 2)  # draw button
        pygame.draw.line(self.surface, self.color, [x+6 for x in self.pos], [x+32 for x in self.pos], 2)
        pygame.draw.line(self.surface, self.color, (self.pos[0]+6, self.pos[1]+32), (self.pos[0]+32, self.pos[1]+6), 2)
        self.surface.blit(self.label,(self.pos[0]+10,self.pos[1]+10))

    def selected(self, pos):
        """ Change the color of the button"""
        if pos:
            self.color = (255, 255, 255)
            self.active = 1
        else:
            self.color = (180, 180, 180)
            self.active = 0

class LoButton():
    def __init__(self, label, surface, pos):
        self.color    = (255, 255, 255)
        self.font     = pygame.font.SysFont('monospace', 18)
        self.label    = self.font.render('%s' % label, False, (255, 255, 255))
        self.surface  = surface
        self.pos      = pos
        self.width    = 40
        self.height   = 40
        self.rect     = pygame.Rect(pos[0], pos[1], self.width, self.height)
        self.counter  = .01
        self.active = 0

    def draw(self):
        ''' Draw to button'''
        self.counter += .01
        if self.counter > 2*3.14:
            self.counter = 0
        pygame.draw.ellipse(self.surface, self.color, self.rect, 2)  # draw button
        t = np.arange(30)+self.pos[0]+5
        x = [int(10*x+self.pos[1]+20) for x in list(np.sin(2*3.14*t*100+self.counter))]
        pygame.draw.lines(self.surface, self.color, 0, zip(t, x), 2)
        self.surface.blit(self.label,(self.pos[0]+10,self.pos[1]+10))

    def selected(self, pos):
        """ Change the color of the button"""
        if pos:
            self.color    = (255, 255, 255)
            self.active = 1
        else:
            self.color    = (180, 180, 180)
            self.active = 0

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
screen=pygame.display.set_mode([1080, 1000])
screen.fill([0, 0, 0])


button_list = {
    1 : GameButton("filters", screen, (100, 100), width=100),
    2 : MixerButton('', screen, (200, 200)),
    3 : LoButton('', screen, (300, 300))
}

signal_window = SignalWindow(screen, (100, 500))
signal_window2 = SignalWindow(screen, (100, 500), color=[0, 255,255])

signal_window3 = SignalWindow(screen, (600, 500), color=[255, 255,255])
counter = 0
freq = 1
phase = 0
en_add = 0
y2 = [.1] * 400
y3 = [.1] * 400
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                freq += -1
            if event.key == pygame.K_RIGHT:
                freq += 1
            if event.key == pygame.K_UP:
                phase += -.1
            if event.key == pygame.K_DOWN:
                phase += .1
            if event.key == pygame.K_a:
                if en_add == 0:
                    en_add = 1
                else:
                    en_add = 0

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            for item in button_list:
                button_list[item].selected(0)
                if button_list[item].rect.collidepoint(mouse_pos):
                    button_list[item].selected(1)
                    print('button was pressed at {0}'.format(mouse_pos))

    # Redraw the background
    counter += .01
    if counter > 1:
        counter = 0
    screen.fill(background_color)
    sample1 = int(50 * np.sin(2*np.pi*freq*counter+phase))
    sample2 = int(50 * np.sin(2*np.pi*freq*counter+1.5))
    y2.insert(0, sample1)
    y3.insert(0, sample2)
    del y2[-1]
    del y3[-1]

    signal_window.draw(zip(range(400), y2))
    signal_window2.draw(zip(range(400), y3))
    y4 = [(x*y)/30 for x,y in zip(y3, y2)]
    y5 = [(x+y) for x,y in zip(y3, y2)]
    if en_add == 1:
        signal_window3.draw(zip(range(400), y5))
    else:
        signal_window3.draw(zip(range(400), y4))
    for item in button_list:
        button_list[item].draw()

    screen.blit(screen, (0, 0))

    pygame.display.flip()

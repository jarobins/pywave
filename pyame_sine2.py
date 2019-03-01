
import pygame, sys
import numpy as np
import math
import time
from pygame.locals import *

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 24)

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
screen=pygame.display.set_mode([1080, 800])
screen.fill([0, 0, 0])
y = [240] * 1024
y2 = [0] * 1024
y3 = [240] * 1024
y4 = [0] * 1024

speed = 1
freq = 1
ddc_freq = 1
counter = 0
ddc_en = 0
ddc_rot_en = 0
ddc_phase = 0

x = [x+20 for x in range(0, 1024)]
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ddc_freq -= 1
            if event.key == pygame.K_RIGHT:
                ddc_freq += 1
            if event.key == pygame.K_UP:
                freq -= 1
            if event.key == pygame.K_DOWN:
                freq += 1
            if event.key == pygame.K_d:
                ddc_en = (ddc_en + 1) % 2
            if event.key == pygame.K_r:
                ddc_phase += .1
            if event.key == pygame.K_t:
                ddc_phase -= .1

    # Redraw the background
    screen.fill(background_color)
    print(ddc_en)

    counter += .01
    sample1 = int(50 * np.sin(2*np.pi*freq*counter))
    sample2 = int(50 * np.cos(2*np.pi*freq*counter))
    cmplx_sample = sample1 + (1j*sample2)

    ddc_sample1 = int(2 * np.sin(2*np.pi*ddc_freq*counter+ddc_phase))
    ddc_sample2 = int(2 * np.cos(2*np.pi*ddc_freq*counter+ddc_phase))
    ddc_cmplx_sample = ddc_sample2 + (1j*ddc_sample1)
    if ddc_en:
        cmplx_sample *= ddc_cmplx_sample
    z = abs((np.fft.fft(y2)/1024))
    z *= z
    z /= 10
    max_x = list(z).index(max(z))
    max_y = max(z)
    z = (-z)+750
    if counter > 1:
        counter = 0

    y.insert(0, cmplx_sample.real+300)
    y2.insert(0, cmplx_sample)
    y3.insert(0, cmplx_sample.imag+450)
    del y[-1]
    del y2[-1]
    del y3[-1]
    pygame.draw.lines(screen, [255, 255, 255], False, zip(x, y), 2)
    pygame.draw.lines(screen, [255, 255, 255], False, zip(x, z), 2)
    pygame.draw.lines(screen, [255, 255, 255], False, zip(x, y3), 2)

    textsurface  = myfont.render('FREQ    : %s' % freq, False, (255, 255, 255))
    textsurface2 = myfont.render('DDC FREQ: %s' % ddc_freq, False, (255, 255, 255))
    textsurface3 = myfont.render('DDC EN  : %s' % ddc_en, False, (255, 255, 255))
    textsurface4 = myfont.render('MAX(%.2f)' % max_y, False, (255, 255, 255))

    screen.blit(screen, (0, 0))
    screen.blit(textsurface,(10,20))
    screen.blit(textsurface2,(10,40))
    screen.blit(textsurface3,(10,60))
    screen.blit(textsurface4,(max_x,700-max_y))
    pygame.display.flip()

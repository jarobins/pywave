
import pygame, sys
import numpy as np
import math
import time
import random
from pygame.locals import *

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 24)

# Just define some colors we can use
color = pygame.Color(255, 255, 0, 0)
background_color = pygame.Color(0, 0, 0, 0)


pygame.init()
screen=pygame.display.set_mode([1080, 1000])
screen.fill([0, 0, 0])

y  = [240] * 1024
y2 = [.1] * 1024
y3 = [240] * 1024
y4 = [.1] * 1024

noise = [random.randint(-100,100) for a in range(1024)]

filter_list = [
    0.000000000000000000,
    0.000002974501611384,
    0.000011630961589138,
    0.000022967232209164,
    0.000030716225059778,
    0.000026214839732923,
    0.000000000000000000,
    -0.000055973251773900,
    -0.000145723873974251,
    -0.000266615935880751,
    -0.000407198371448263,
    -0.000546075600414797,
    -0.000652361272314452,
    -0.000688147432914718,
    -0.000613179612975004,
    -0.000391575659878668,
    0.000000000000000001,
    0.000563732118198938,
    0.001273013656973618,
    0.002067373906878073,
    0.002851563067893035,
    0.003500082348355214,
    0.003867862608841334,
    0.003806962971094718,
    0.003188176579066728,
    0.001925429347868523,
    -0.000000000000000002,
    -0.002518961647177852,
    -0.005461249814074702,
    -0.008552964568398333,
    -0.011426676391665728,
    -0.013645225159174835,
    -0.014738246181366184,
    -0.014248680591636921,
    -0.011784851782051391,
    -0.007072431628762949,
    0.000000000000000003,
    0.009347935765629322,
    0.020675604354698812,
    0.033481714360691445,
    0.047087359848541926,
    0.060684558865161380,
    0.073401325498431910,
    0.084376989102916758,
    0.092839977176476990,
    0.098179693861485506,
    0.100004559152954045,
    0.098179693861485506,
    0.092839977176476990,
    0.084376989102916772,
    0.073401325498431910,
    0.060684558865161380,
    0.047087359848541920,
    0.033481714360691452,
    0.020675604354698819,
    0.009347935765629319,
    0.000000000000000003,
    -0.007072431628762950,
    -0.011784851782051391,
    -0.014248680591636925,
    -0.014738246181366184,
    -0.013645225159174839,
    -0.011426676391665735,
    -0.008552964568398330,
    -0.005461249814074704,
    -0.002518961647177853,
    -0.000000000000000002,
    0.001925429347868524,
    0.003188176579066726,
    0.003806962971094720,
    0.003867862608841335,
    0.003500082348355213,
    0.002851563067893038,
    0.002067373906878075,
    0.001273013656973618,
    0.000563732118198938,
    0.000000000000000001,
    -0.000391575659878668,
    -0.000613179612975004,
    -0.000688147432914718,
    -0.000652361272314452,
    -0.000546075600414798,
    -0.000407198371448264,
    -0.000266615935880751,
    -0.000145723873974251,
    -0.000055973251773899,
    0.000000000000000000,
    0.000026214839732923,
    0.000030716225059778,
    0.000022967232209164,
    0.000011630961589138,
    0.000002974501611384,
    0.000000000000000000,
]
filter_len  = 93
filter_data = [0] * filter_len

speed          = 1
freq           = 1
ddc_freq       = 1
counter        = 0
ddc_en         = 0
ddc_rot_en     = 0
ddc_phase      = 0
filter_menu_en = 0

filter_button  = pygame.Rect(20, 780, 150, 40)
filter_button1 = pygame.Rect(200, 780, 150, 40)
filter_menu    = pygame.Rect(200, 400, 400, 600)

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
                ddc_phase += .01
            if event.key == pygame.K_t:
                ddc_phase -= .01
            if event.key == pygame.K_f:
                filter_menu_en = (filter_menu_en + 1) % 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if filter_button.collidepoint(mouse_pos):
                # prints current location of mouse
                print('button was pressed at {0}'.format(mouse_pos))

    # Redraw the background
    screen.fill(background_color)

    counter += .01
    sample1 = int(50 * np.sin(2*np.pi*freq*counter))
    sample2 = int(50 * np.cos(2*np.pi*freq*counter))
    cmplx_sample = sample1 + (1j*sample2)

    ddc_sample1 = int(2 * np.sin(2*np.pi*ddc_freq*counter+ddc_phase))
    ddc_sample2 = int(2 * np.cos(2*np.pi*ddc_freq*counter+ddc_phase))
    ddc_cmplx_sample = ddc_sample2 + (1j*ddc_sample1)
    if ddc_en:
        cmplx_sample *= ddc_cmplx_sample
    y2 = [a+b for a,b in zip(y2, noise)]
    z = abs((np.fft.fft([(2**8)*a for a in y2]))/1024)**2
    z = 20*np.log10(z)
    max_x = list(z).index(max(z))
    max_y = max(z)
    z = (-z)+750
    if counter > 1:
        counter = 0

    y.insert(0, y2[0].real+300)
    y3.insert(0, y2[0].imag+450)
    noise.insert(0, random.randint(-100, 100)*.0001+(1j*random.randint(-100, 100)*.0001))

    del y[-1]
    del y3[-1]
    del noise[-1]

    if filter_menu_en == 0:
        y2.insert(0, cmplx_sample)
        del y2[-1]
    else:
        filter_sample = 0
        filter_data.insert(0, cmplx_sample)
        del filter_data[-1]
        for num,b in enumerate(zip(filter_list, filter_data)):
            filter_sample = filter_sample + (b[0] * b[1])
        y2.insert(0, filter_sample)
        del y2[-1]

    pygame.draw.lines(screen, [255, 255, 255], False, [a for a in zip(x, y)], 2)
    pygame.draw.lines(screen, [255, 255, 255], False, [a for a in zip(x, z)], 2)
    pygame.draw.lines(screen, [255, 255, 255], False, [a for a in zip(x, y3)], 2)

    textsurface  = myfont.render('FREQ    : %s' % freq, False, (255, 255, 255))
    textsurface2 = myfont.render('DDC FREQ: %s' % ddc_freq, False, (255, 255, 255))
    textsurface3 = myfont.render('DDC EN  : %s' % ddc_en, False, (255, 255, 255))
    textsurface4 = myfont.render('%.2fHz(%.2f)' % (max_x*(100.0/1024), max_y), False, (255, 255, 255))
    textsurface5 = myfont.render('DDC PHAS: %s' % ddc_phase, False, (255, 255, 255))
    textsurface6 = myfont.render('Filters', False, (255, 255, 255))

    pygame.draw.rect(screen, [255, 255, 255], filter_button, 2)  # draw button

    screen.blit(screen, (0, 0))
    screen.blit(textsurface,(10,20))
    screen.blit(textsurface2,(10,40))
    screen.blit(textsurface3,(10,60))
    screen.blit(textsurface5,(10,80))
    screen.blit(textsurface6,(47,786))
    screen.blit(textsurface4,(max_x,700-max_y))
    pygame.display.flip()

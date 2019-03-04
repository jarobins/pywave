import math
import pyglet
import numpy as np
from pyglet.gl import *

win = pyglet.window.Window()

# get all the points in a circle centered at 0.
def PointsInCircum(r, n=25, pi=3.14):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
t = [x*.1 for x in range(1000)]
pts = np.array([100*math.sin(x*3.14*2) for x in t])

# function that increments to the next
# point along a circle
frame = 0
def update_frame(x, y):
    global frame
    if frame > 100:
        frame = 0
    else:
        frame += 1

@win.event
def on_draw():
    # clear the screen
    glClear(GL_COLOR_BUFFER_BIT)
    # draw the next line
    # in the circle animation
    # circle centered at 100,100,0 = x,y,z
    glBegin(GL_LINES)
    for x in range(100):
        glVertex3f(pts[frame]+200+x,100+x,0)
    glEnd()

# every 1/10 th get the next frame
pyglet.clock.schedule(update_frame, 1/10.0)
pyglet.app.run()

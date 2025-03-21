import pygame
from OpenGL.raw.GL.VERSION.GL_1_0 import GL_PROJECTION
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode(size=(screen_width, screen_height), flags=DOUBLEBUF | OPENGL)
pygame.display.set_caption('Primeiro OpenGL')

def init_ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 440, 0, 480)

def draw_star(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()
    
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True 
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_star(231, 151, 10)
    draw_star(200, 200, 20)
    glEnd()
    
    pygame.display.flip()
    pygame.time.wait(100)
pygame.quit()
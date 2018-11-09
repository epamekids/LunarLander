import pygame
import math
#import sys

SCREEN_SIZE = [1024,768]

WHITE = [255,255,255]
RED   = [255,  0,  0]
GREEN = [  0,255,  0]
BLUE  = [  0,  0,255]
BLACK = [  0,  0,  0]

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
font = pygame.font.SysFont('Consolas', 25)

angle = 0
R = 200
(x1,y1) = (0,0)

run = True
while (run):
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            angle -= 1
        if event.key == pygame.K_RIGHT:
            angle += 1


    pygame.display.flip()
    pygame.time.wait(10)

while (True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

pygame.quit()
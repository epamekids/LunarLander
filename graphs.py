import pygame

SCREEN_SIZE = [1024,768]

def coord(xy):
    global SCREEN_SIZE
    x = xy[0]
    y = -xy[1] + SCREEN_SIZE[1]
    return (int(x),int(y))

WHITE = [255,255,255]
RED   = [255,  0,  0]
GREEN = [  0,255,  0]
BLUE  = [  0,  0,255]
BLACK = [  0,  0,  0]

pygame.display.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill((255, 255, 255))

pygame.draw.line(screen, GREEN, (0, SCREEN_SIZE[1]/2), (SCREEN_SIZE[0], SCREEN_SIZE[1]/2))
pygame.draw.line(screen, RED, (0, SCREEN_SIZE[1]), (SCREEN_SIZE[0], SCREEN_SIZE[1]))
pygame.display.update()

t = 0.01

G = 6.6740831e-11
Mm = 7.3477e22
Rm = 1737100
g1 = -G * Mm

T = 0
H = 0
V = 0
Md = 4600
Mf = 2000
Ft = 45000
Vf = 3050
Mt = Ft / Vf

while H >= 0:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        break
    Ma = Md + Mf
    if (Mf > (Mt*t)):
        Mf = Mf - Mt * t
        ae = Ft/Ma
    else:
        ae = 0

    g = g1 / (Rm + H)**2
    a = ae + g
    V = V + a * t
    H = H + V * t
    T = T + t
    if (abs(T - round(T)) <= t / 2):
        print ('T=' + str(T) + " s;" + " Mf=" + str(Mf) + " H=" + str(H) + " m;" + " V=" + str(V) + " m/s;" + " a=" + str(a) + " m/s^2")
        pygame.draw.circle(screen, RED,
                           coord((T * SCREEN_SIZE[0] / 1700, Mf * SCREEN_SIZE[1] / 2000)), 3, 3)
        pygame.draw.circle(screen, BLUE,
                           coord((T * SCREEN_SIZE[0] / 1700, H * SCREEN_SIZE[1] / 360000)), 3, 3)
        pygame.draw.circle(screen, GREEN,
                           coord((T*SCREEN_SIZE[0]/1700, V*SCREEN_SIZE[1]/2000+SCREEN_SIZE[1]/2)), 3, 3)
        pygame.draw.circle(screen, BLACK,
                           coord((T*SCREEN_SIZE[0]/1700, a*SCREEN_SIZE[1]/20+SCREEN_SIZE[1]/2)), 3, 3)
        pygame.display.update()

print ('T=' + str(T) + " s;" + " Mf=" + str(Mf) + " H=" + str(H) + " m;" + " V=" + str(V) + " m/s;" + " a=" + str(a) + " m/s^2")

while (True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break
pygame.quit()

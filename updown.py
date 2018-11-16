import pygame

SCREEN_SIZE = [800,600]

def coord(xy):
    global SCREEN_SIZE
    x = xy[0]
    y = SCREEN_SIZE[1]-xy[1]
    return (x,y)

WHITE = [255,255,255]
RED   = [255,  0,  0]
GREEN = [  0,255,  0]
BLUE  = [  0,  0,255]
BLACK = [  0,  0,  0]

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
bg = pygame.image.load('back.jpg')
bg = pygame.transform.scale(bg, SCREEN_SIZE)
imgF = pygame.image.load('rocket4sf.png').convert_alpha()
imgNF = pygame.image.load('rocket4s.png').convert_alpha()
imgB = pygame.image.load('boom.png').convert_alpha()
imgF.set_alpha(1)
imgNF.set_alpha(1)
imgB.set_alpha(1)
font = pygame.font.SysFont('Consolas', 25)

t = 0.01

G = 6.6740831e-11
Mm = 7.3477e22
Rm = 1737100
g1 = -G * Mm

T = 0
H = 0
V = 0
Md = 4600
Mf = 1000
Ft = 45000
Vf = 3050
Kt = 1

clock=pygame.time.Clock()
run = True
while (run):
    dt = clock.tick(100)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if Kt > 0:
                Kt = 0
            else:
                Kt = 1

    screen.fill(WHITE)

    for i in range(1,int(dt/10)+1):
        Fte = Ft* Kt
        Mt = Fte / Vf
        if H >= 0:
            Ma = Md + Mf
            if (Mf > (Mt*t)):
                Mf = Mf - Mt * t
                ae = Fte/Ma
                if Kt > 0:
                    img = imgF
                else:
                    img = imgNF
            else:
                ae = 0
                img = imgNF

            g = g1 / (Rm + H)**2
            a = ae + g
            V = V + a * t
            H = H + V * t
            T = T + t
        else:
            run = False
            if (abs(V) > 10):
                img = imgB

    screen.blit(bg, (0, 0))
    screen.blit(img, coord((SCREEN_SIZE[0]/2, int(H * SCREEN_SIZE[1] / 5000)+56)))
    screen.blit(font.render('Height  : ' + '{:>7.0f}'.format(H) + ' m', True, WHITE), (25, 25))
    screen.blit(font.render('Velocity: ' + '{:>7.2f}'.format(V) + ' m/s', True, WHITE), (25, 50))
    screen.blit(font.render('Accel.  : ' + '{:>7.2f}'.format(a) + ' m/s^2', True, WHITE), (25, 75))
    screen.blit(font.render('Fuel    : ' + '{:>7.0f}'.format(Mf) + ' kg', True, WHITE), (25, 100))
    screen.blit(font.render('T/W     : ' + '{:>7.2f}'.format(-ae/g), True, WHITE), (25, 125))
    screen.blit(font.render('Time    : ' + '{:>7.0f}'.format(T) + ' s', True, WHITE), (25, 150))
    pygame.display.flip()

while (True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

pygame.quit()

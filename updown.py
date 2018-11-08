import pygame

SCREEN_SIZE = [1024,768]

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
bg = pygame.image.load("back.jpg")
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
Mf = 2000
Ft = 15000
Vf = 3050
Mt = Ft / Vf

run = True
while (run):
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        run = False
    screen.fill(WHITE)

    for i in range(1,100):
        if H >= 0:
            Ma = Md + Mf
            if (Mf > (Mt*t)):
                Mf = Mf - Mt * t
                ae = Ft/Ma
                img = imgF
            else:
                ae = 0
                img = imgNF

            g = g1 / (Rm + H)**2
            a = ae + g
            V = V + a * t
            H = H + V * t
            T = T + t
#            if (abs(T - round(T)) <= t / 2):
#                print ('T=' + str(T) + " s;" + " Mf=" + str(Mf) + " H=" + str(H) + " m;" + " V=" + str(V) + " m/s;" + " a=" + str(a) + " m/s^2")
        else:
            run = False
            if (abs(V) > 7.5):
                img = imgB
#            break
    screen.blit(bg, (0, 0))
    screen.blit(img, coord((240, int(H * 768 / 400000)+68)))
    screen.blit(font.render('Height:' + str("%.2f" % round(H,2) + 'm'), True, WHITE), (200, 50))
    screen.blit(font.render('Velocity:' + str("%.2f" % round(V, 2) + 'm/s'), True, WHITE), (200, 100))
    screen.blit(font.render('Acceleration:' + str("%.2f" % round(a, 2) + 'm/s^2'), True, WHITE), (200, 150))
    screen.blit(font.render('Fuel:' + str("%.2f" % round(Mf, 2) + 'kg'), True, WHITE), (200, 200))
    pygame.display.flip()
    pygame.time.wait(10)

#    print ('T=' + str(T) + " s;" + " Mf=" + str(Mf) + " H=" + str(H) + " m;" + " V=" + str(V) + " m/s;" + " a=" + str(a) + " m/s^2")

pygame.time.wait(1000)
pygame.quit()
import pygame
import math

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

G = 6.6740831e-11 # гравитационная постоянная
Mm = 7.3477e22 # масса Луны kg
Rm = 1737100 # радиус Луны m
g1 = -G * Mm

T = 0 # время
H = 0 # начальная высота
L = 0 # начальная дистанция
Vv = 0 # начальная вертикальная скорость
Vh = 0 # начальная горизонтальная скорость
A = 45 # начальный угол наклона тяги (в градусах)
Md = 4600 # Масса нашего корабля без топлива
Mf = 300 # Масса топлива - недозаправлен
Ft = 45000 # Сила тяги двигателя в N
Vf = 3050 # Скорость истечения топлива из двигателя
Kt = 1 # текущая тяга двигателя относительно полной от 0 (выключен) до 1 (полная)

clock=pygame.time.Clock()
run = True
while (run):
#    dt = clock.tick(100)
    dt = 100 ; pygame.time.wait(10) # чтобы не очень медленно, но ине улетало сразу в бесконечность
    event = pygame.event.poll()
    if event.type == pygame.QUIT: # если нажали закрыть окно
        run = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if Kt > 0:
                Kt = 0
            else:
                Kt = 1

    screen.fill(WHITE)

    for i in range(1,int(dt/10)+1):
        Fte = Ft* Kt # эффективная тяга двигателя
        Mt = Fte / Vf # расход топлива в секунду
        if H >= 0:
            Ma = Md + Mf # полная масса корабля - сухая + топливо
            if (Mf > (Mt*t)): # хватит ли нам топлива на время t
                Mf = Mf - Mt * t # новая масса топлива
                ae = Fte/Ma # ускорение от двигателя
                if Kt > 0:
                    img = imgF
                else:
                    img = imgNF
            else: # топливо закончилось
                ae = 0
                img = imgNF

            g = g1 / (Rm + H)**2 # ускорение свободного падения на Луне для высоты H
            # раскладываем ускорение от двигателя ae под углом A на горизонтальное и вертикальное. Не забываем про единицы угла
            av =  # вертикальное ускорение
            ah =  # горизонтальное ускорение
            av = av + g # по вертикали на нас действует еще одна сила
            ah = ah     # по горизонтали никаких других сил нет
            Vv = Vv + av * t # новая вертикальная скорость
            Vh = # новая горизонтальная скорость
            H = H + Vv * t # новая высота
            L = # новая дистанция
            T = T + t
        else:
            run = False
            if (abs(Vv) > 10):
                img = imgB

    screen.blit(bg, (0, 0))
    screen.blit(img, coord((L*SCREEN_SIZE[0]/ 50000+10, int(H * SCREEN_SIZE[1] / 50000)+56)))
    screen.blit(font.render('Height  : ' + '{:>7.0f}'.format(H) + ' m', True, WHITE), (25, 25))
    screen.blit(font.render('Dist.   : ' + '{:>7.0f}'.format(L) + ' m', True, WHITE), (SCREEN_SIZE[0]/2+25, 25))
    screen.blit(font.render('Vel. v. : ' + '{:>7.2f}'.format(Vv) + ' m/s', True, WHITE), (25, 50))
    screen.blit(font.render('Vel. h. : ' + '{:>7.2f}'.format(Vh) + ' m/s', True, WHITE), (SCREEN_SIZE[0] / 2 + 25, 50))
    screen.blit(font.render('Accel. v: ' + '{:>7.2f}'.format(av) + ' m/s^2', True, WHITE), (25, 75))
    screen.blit(font.render('Accel. h: ' + '{:>7.2f}'.format(ah) + ' m/s^2', True, WHITE), (SCREEN_SIZE[0] / 2 + 25, 75))
    screen.blit(font.render('Fuel    : ' + '{:>7.0f}'.format(Mf) + ' kg', True, WHITE), (25, 100))
    screen.blit(font.render('T/W     : ' + '{:>7.2f}'.format(-ae/g), True, WHITE), (25, 125))
    screen.blit(font.render('Time    : ' + '{:>7.0f}'.format(T) + ' s', True, WHITE), (25, 150))
    pygame.display.flip()

while (True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

pygame.quit()

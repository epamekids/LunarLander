import pygame
import math

SCREEN_SIZE = [800,600]

def coord(xy):
    global SCREEN_SIZE
    x = int(xy[0])
    y = SCREEN_SIZE[1]-int(xy[1])
    return (x,y)

WHITE = [255,255,255]
RED   = [255,  0,  0]
GREEN = [  0,255,  0]
BLUE  = [  0,  0,255]
GREY  = [127,127,127]
BLACK = [  0,  0,  0]

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
track_screen = screen.copy()
track_screen.set_colorkey(BLACK)
track_screen.fill(BLACK)
bg = pygame.image.load('back.jpg')
bg = pygame.transform.scale(bg, SCREEN_SIZE)
imgF = pygame.image.load('rocket3sf.png').convert_alpha()
imgNF = pygame.image.load('rocket3s.png').convert_alpha()
imgB = pygame.image.load('boom.png').convert_alpha()
imgF.set_alpha(1)
imgNF.set_alpha(1)
imgB.set_alpha(1)
font = pygame.font.SysFont('Consolas', 25)

track_height = 10

def draw_button(state):
    screen = pygame.Surface((track_height*4 + font.size('TRK')[0],track_height*2))
    if (state):
        BUT_COLOR = GREEN
        track_sw = 0 + track_height + track_height + track_height // 2
    else:
        BUT_COLOR = GREY
        track_sw = 0 + track_height
    pygame.draw.circle(screen, BUT_COLOR, (0 + track_height, 0 + track_height), track_height)
    pygame.draw.rect(screen, BUT_COLOR,
                 (track_height, 0, track_height + track_height // 2, track_height * 2))
    pygame.draw.circle(screen, BUT_COLOR, (0 + track_height * 2 + track_height // 2, 0 + track_height), track_height)
    pygame.draw.circle(screen, WHITE, (track_sw, 0 + track_height), track_height - 1)
    screen.blit(font.render('TRK', True, BUT_COLOR), (0 + track_height + track_height*3, 0))
    return screen

def draw_fuel(percent):
    for i in range(0, percent):
        pygame.draw.line(screen, RED, (500,500-i), (510, 500-i))

track_button_on = draw_button(True)
track_button_off = draw_button(False)
track_pos = (400,400)

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
Mf = 4000 # Масса топлива - недозаправлен
Ft = 45000 # Сила тяги двигателя в N
Vf = 3050 # Скорость истечения топлива из двигателя
Kt = 1 # текущая тяга двигателя относительно полной от 0 (выключен) до 1 (полная)

clock=pygame.time.Clock()
track = False
run = True
while (run):
#    dt = clock.tick(100)
    dt = 100 ; pygame.time.wait(10) # чтобы не очень медленно, но и не улетало сразу в бесконечность
    event = pygame.event.poll()
    if event.type == pygame.QUIT: # если нажали закрыть окно
        run = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if Kt > 0:
                Kt = 0
            else:
                Kt = 1
        if event.key == pygame.K_LEFT:
            A = A - 1
        if event.key == pygame.K_RIGHT:
            A = A + 1
    if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
        m_x, m_y = event.pos
        if ((m_x >= track_pos[0]) and
            (m_x <= (track_pos[0] + track_height * 4)) and
            (m_y >= track_pos[1]) and
            (m_y <= (track_pos[1] + track_height * 2))):
            track = not track

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
            # раскладываем ускорение от двигвтеля ae под углом A на горизонтальное и вертикальное. Не забываем про единицы угла
            av = ae * math.cos(math.radians(A))# вертикальное ускорение
            ah = ae * math.sin(math.radians(A))# горизонтальное ускорение
            av = av + g # по вертикали на нас действует еще одна сила
            ah = ah     # по горизонтали никаких других сил нет
            Vv = Vv + av * t # новая вертикальная скорость
            Vh = Vh + ah * t # новая горизонтальная скорость
            H = H + Vv * t # новая высота
            L = L + Vh * t # новая дистанция
            T = T + t
        else:
            run = False
            if (abs(Vv) > 10):
                img = imgB

    img = pygame.transform.rotate(img, 360-A)
    screen.fill(WHITE)
    screen.blit(bg, (0, 0))

    pygame.draw.circle(track_screen, BLUE, coord(
        (L * SCREEN_SIZE[0] / 50000 + 10 + img.get_width() // 2, H * SCREEN_SIZE[1] / 50000 + 64 - img.get_height()//2)), 0)
    if (track):
        screen.blit(track_screen, (0, 0))

    if (track):
        track_button = track_button_on
    else:
        track_button = track_button_off
    screen.blit(track_button, track_pos)

#    draw_fuel(int(Mf*100/14000))
    screen.blit(img, coord((L*SCREEN_SIZE[0]/ 50000+10, H * SCREEN_SIZE[1] / 50000+40+img.get_height())))
    screen.blit(font.render('Height  : ' + '{:>7.0f}'.format(H) + ' m', True, WHITE), (25, 25))
    screen.blit(font.render('Dist.   : ' + '{:>7.0f}'.format(L) + ' m', True, WHITE), (SCREEN_SIZE[0]/2+25, 25))
    screen.blit(font.render('Vel. v. : ' + '{:>7.2f}'.format(Vv) + ' m/s', True, WHITE), (25, 50))
    screen.blit(font.render('Vel. h. : ' + '{:>7.2f}'.format(Vh) + ' m/s', True, WHITE), (SCREEN_SIZE[0] / 2 + 25, 50))
    screen.blit(font.render('Accel. v: ' + '{:>7.2f}'.format(av) + ' m/s^2', True, WHITE), (25, 75))
    screen.blit(font.render('Accel. h: ' + '{:>7.2f}'.format(ah) + ' m/s^2', True, WHITE), (SCREEN_SIZE[0] / 2 + 25, 75))
    screen.blit(font.render('Fuel    : ' + '{:>7.0f}'.format(Mf) + ' kg', True, WHITE), (25, 100))
    screen.blit(font.render('Angle   : ' + '{:>7.0f}'.format(A) + ' deg', True, WHITE), (SCREEN_SIZE[0] / 2 + 25, 100))
    screen.blit(font.render('T/W     : ' + '{:>7.2f}'.format(-ae/g), True, WHITE), (25, 125))
    screen.blit(font.render('Time    : ' + '{:>7.0f}'.format(T) + ' s', True, WHITE), (25, 150))
    pygame.display.flip()

while (True):
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        break

pygame.quit()
from re import T
from tracemalloc import start
from cv2 import cvtColor
from vehicles_ising import *
import cv2 as cv
import random
import numpy as np
import pygame
import sys


altura = 500
largura = 500
gray = (50, 50, 50)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
background = white
ball_color = gray


fps = 60
T = 5
if len(sys.argv) != 2:
    print("Error Usage. You must type this form: python main.py path_image")
else:
    filename = sys.argv[1]
    # img = cv.imread("assets/alexia.png")
    img = cv.imread(filename)
    img = cv.resize(img, [500, 500])
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    print(img.shape)
    t = 0
    bs = []
    particules = []
    on_move = set()
    for i in range(0, len(img_gray), 4):
        for j in range(0, len(img_gray[i]), 4):
            bs.append(float(img_gray[i][j]))
            b = 256 - float(img_gray[i][j])
            color = img[i][j]
            color[0], color[-1] = color[-1], color[0]
            raio = (b / 255) * 4
            if raio >= 1.9:
                particules.append(Particle(raio, j, i, ball_color))
    print(len(particules))
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 10)
    to_play = [
        font.render(f'Press "M" to increase 1 on temperature', True, red),
        font.render(f'Press "U" to increase 0.1 on temperature', True, red),
        font.render(f'Press "N" to decrease 1 on temperature', True, red),
        font.render(f'Press "D" to decrease 0.1 on temperature', True, red)
    ]
    relogio = pygame.time.Clock()
    window = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Steering Behaviors")
    window.fill(gray)
    continua = True
    while continua:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continua = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continua = False
                if event.key == pygame.K_r:
                    for v in particules:
                        v.position = pygame.Vector2(v.initial_position)
                if event.key == pygame.K_u:
                    T += 0.1
                    print(T)
                if event.key == pygame.K_d:
                    T -= 0.1
                    print(T)

                if event.key == pygame.K_m:
                    T += 1
                    print(T)

                if event.key == pygame.K_n:
                    T -= 1
                    print(T)
        
        window.fill(background)

        for v in particules:
            v.seek(target=v.initial_position, T=T)
            pygame.draw.circle(window, v.color, v.position, v.b)


        for i in range(len(to_play)):
            window.blit(to_play[i], (20, 20 + i * 10))
        T_w = font.render(f'Temperature = {T:.2f}', True, red)
        window.blit(T_w, (20, 70))
        t += 1
        relogio.tick(fps)
        pygame.display.update()
    pygame.quit()




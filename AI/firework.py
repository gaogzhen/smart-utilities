import math

import pygame
import random
from pygame.locals import *

# 初始化Pygame
pygame.init()

# 设置屏幕大小
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# 设置标题
pygame.display.set_caption('烟花显示')

# 定义颜色
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255)
]

class Firework:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.particles = []

        for _ in range(100):
            angle = random.uniform(0, 2 * 3.1415)
            speed = random.uniform(1, 5)
            dx = speed * math.cos(angle)
            dy = speed * math.sin(angle)
            self.particles.append([x, y, dx, dy])

    def update(self):
        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]
            particle[3] += 0.1

    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, self.color, (int(particle[0]), int(particle[1])), 3)

# 事件循环
fireworks = []
clock = pygame.time.Clock()
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            color = random.choice(colors)
            fireworks.append(Firework(x, y, color))

    for firework in fireworks:
        firework.update()
        firework.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

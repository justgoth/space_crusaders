import pygame
from pygame.locals import *
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, type, x, y, angle, pos):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.rect = pygame.Rect(x, y, 10, 10)
        if type == 5:
            self.speed = 5
            self.pos = pos
        else:
            self.speed = float(10)
            self.pos = float(0)
        self.angle = angle

    def move(self):
        if self.type != 5:
            self.rect.y -= self.speed
        self.pos = self.pos + self.speed
        if self.type == 2:
            self.speed = self.speed * 1.1
        if self.type == 3:
            self.speed = self.speed * 1.2
        if self.type == 4:
            self.speed = self.speed * 10 / random.randint(5, 15)


class Bullets():
    def __init__(self):
        self.bullets = []
        self.enemybullets = []
        self.images = []
        self.images.append(pygame.image.load("resources/sprites/bullet01.png").convert())
        self.images.append(pygame.image.load("resources/sprites/bullet02.png").convert())
        self.images.append(pygame.image.load("resources/sprites/bullet03.png").convert())
        self.images.append(pygame.image.load("resources/sprites/bullet04.png").convert())
        self.images.append(pygame.image.load("resources/sprites/bullet05.png").convert())
        for image in self.images:
            image.set_colorkey(image.get_at((0,0)))

    def add(self, bullet):
        if bullet!=None:
            self.bullets.append(bullet)

    def addenemybullet(self, bullet):
        if bullet!=None:
            self.enemybullets.append(bullet)

    def remove(self, bullet):
        self.bullets.remove(bullet)

    def removeenemybullet(self, bullet):
        self.enemybullets.remove(bullet)

    def move(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.rect.y < 20:
                self.remove(bullet)
        for bullet in self.enemybullets:
            bullet.move()
            if bullet.pos > 1000:
                self.removeenemybullet(bullet)

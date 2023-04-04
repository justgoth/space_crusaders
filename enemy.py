import pygame
from pygame.locals import *
import random
import math
from bullet import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.rect = pygame.Rect(x - 100, y - 100, 200, 200)
        self.scale = float(1)
        self.scalemulty = float(1)
        self.angleinc = float(random.randint(-15, 16)) / 10
        self.angle = float(random.randint(0, 359))
        self.life = 100
        self.suffering = 50

    def move(self):
        self.angle += self.angleinc
        self.angleinc += float(random.randint(-3, 4)) / 10
        if self.angleinc > 2:
            self.angleinc = 2
        if self.angleinc < -2:
            self.angleinc = -2
        self.scalemulty = abs(self.scalemulty + random.randint(-2, 3) / random.randint(10, 30))
        if self.scalemulty < 0.9:
            self.scalemulty = 0.9
        if self.scalemulty > 1.05:
            self.scalemulty = 1.05
        self.scale *= self.scalemulty**(1/4)
        if self.scale < 0.5:
            self.scale = 0.5
        if self.scale > 0.8:
            self.scale = 0.8
        if random.randint(1, 1000) == 1:
            bullet = Bullet(5, self.rect.centerx, self.rect.centery, self.angle / (2*math.pi), self.scale*100)
            return bullet
        if self.suffering < 50:
            self.suffering = self.suffering - 1
        if self.suffering == 0:
            self.suffering = 50

    def suffer(self):
        if self.life > 0:
           self.life -= 20
           self.suffering = 40

class Enemies():
    def __init__(self):
        self.enemies = []
        self.images = []
        self.images.append(pygame.image.load("resources/sprites/enemy01.jpg").convert())
        for image in self.images:
            image.set_colorkey(image.get_at((0,0)))
        self.x = 0
        self.y = 0
        self.dx = 1
        self.dy = 1

    def add(self, enemy):
        self.enemies.append(enemy)

    def remove(self, enemy):
        self.enemies.remove(enemy)

    def move(self, bullets, sound):
        self.x += self.dx
        if self.x > 50 or self.x < -50:
            self.dx = -self.dx
        if (random.randint(1, 100) == 50):
            self.dx = -self.dx
        if (random.randint(1, 100) == 50):
            self.dy = -self.dy
        self.y -= self.dy
        if self.y > 50 or self.y < -50:
            self.dy = -self.dy
        for enemy in self.enemies:
            bullet = enemy.move()
            if bullet!=None:
                bullet.rect.x += self.x
                bullet.rect.y += self.y
                bullets.addenemybullet(bullet)
                sound.play()
            if enemy.life <= 0 and enemy.suffering == 50:
                self.remove(enemy)


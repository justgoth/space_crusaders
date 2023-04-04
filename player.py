import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("resources/sprites/player.png").convert_alpha()
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect(center=(960, 900))
        self.speed = float(0)
        self.life = 200
        self.bullettype = 1
        self.suffering = 50

    def move(self, direction):
        if direction == 1:
            self.speed = max(1, self.speed)*1.5
        if direction == -1:
            self.speed = min(-1, self.speed)*1.5
        self.speed = self.speed / 1.15
        if 200 <= self.rect.x <= 1700:
            self.rect.x += self.speed
        if self.rect.x <= 200: self.rect.x = 210
        if self.rect.x >= 1570: self.rect.x = 1560
        if self.suffering < 50:
            self.suffering -= 1
        if self.suffering == 0:
            self.suffering = 50

    def suffer(self):
        if self.life > 0:
           self.life -= 20
           self.suffering = 40


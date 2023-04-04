import pygame
import sys
import random
import math
from pygame.locals import *
from pygame.rect import Rect
from player import Player
from bullet import Bullets, Bullet
from enemy import Enemies, Enemy
from spritesheet import SpriteSheet


class Game():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init();
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.enemies = Enemies()
        self.player = Player()
        self.bullets = Bullets()

        self.background = pygame.image.load('resources/background/01.png')
        self.clock = pygame.time.Clock()
        for x in range(-4, 5, 1):
            for y in range(-1, 2, 1):
                enemy = Enemy(0, 960 + x * 175, 400 + y * 200)
                self.enemies.add(enemy)
        self.brun = 0

        boomsh = SpriteSheet("resources/sprites/boom.png")
        boomrects = []
        for y in range(6):
            for x in range(8):
                boomrect = (x * 150, y * 145, 150, 145)
                boomrects.append(boomrect)
        self.boomsprites = boomsh.images_at(boomrects, -1)
        self.s_boom = pygame.mixer.Sound("resources/sounds/boom.wav")
        self.s_b1 = pygame.mixer.Sound("resources/sounds/bullet00.wav")
        self.s_b2 = pygame.mixer.Sound("resources/sounds/bullet01.wav")
        self.s_b3 = pygame.mixer.Sound("resources/sounds/bullet02.wav")
        self.s_b4 = pygame.mixer.Sound("resources/sounds/bullet03.wav")
        self.s_eb = pygame.mixer.Sound("resources/sounds/enemybullet.wav")

    def input(self, events):
        for event in events:
            if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit(0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)
        if keys[pygame.K_SPACE]:
                if self.brun == 0:
                   bullet = Bullet(self.player.bullettype, self.player.rect.centerx-10, self.player.rect.y - 10, 0, 0)
                   self.bullets.add(bullet)
                   if (self.player.bullettype == 1):
                       self.s_b1.play()
                   if (self.player.bullettype == 2):
                       self.s_b2.play()
                   if (self.player.bullettype == 3):
                       self.s_b3.play()
                   if (self.player.bullettype == 4):
                       self.s_b4.play()
                   self.brun = 5
                else:
                    self.brun -= 1
                    if self.brun < 0:
                        self.brun = 0
        else:
            self.brun -= 1
            if self.brun < 0:
                self.brun = 0
        if keys[pygame.K_1]:
            self.player.bullettype = 1
        if keys[pygame.K_2]:
            self.player.bullettype = 2
        if keys[pygame.K_3]:
            self.player.bullettype = 3
        if keys[pygame.K_4]:
            self.player.bullettype = 4

    def step(self):
        self.screen.blit(self.background, (0, 0))
        self.player.move(0)
        self.bullets.move()
        scale = abs(self.player.speed)**(1/10)
        if scale < 1:
            scale = 1
        if scale > 1.5:
            scale = 1.5
        tblit = pygame.transform.scale(self.player.image, (self.player.image.get_width() / scale, self.player.image.get_height()))
        tblit.set_colorkey(tblit.get_at((0,0)))
        self.screen.blit(tblit, (self.player.rect.centerx - 76, self.player.rect.centery - 75, 153, 150))
        self.enemies.move(self.bullets, self.s_eb)
        for enemy in self.enemies.enemies:
            if enemy.life > 0:
                tblit = pygame.transform.rotate(self.enemies.images[enemy.type], enemy.angle);
                tblit = pygame.transform.scale(tblit, (tblit.get_width() * enemy.scale, tblit.get_height() * enemy.scale))
                rect = tblit.get_rect(center=enemy.rect.center)
                self.screen.blit(tblit, (rect.x + self.enemies.x, rect.y + self.enemies.y))
        for bullet in self.bullets.bullets:
            collide = False
            if bullet.type == 1:
                self.screen.blit(self.bullets.images[bullet.type - 1], bullet.rect)
                for enemy in self.enemies.enemies:
                    trect = pygame.Rect(enemy.rect.x + self.enemies.x, enemy.rect.y + self.enemies.y, enemy.rect.width, enemy.rect.height)
                    if trect.colliderect(bullet.rect):
                        enemy.suffer()
                        self.s_boom.play()
                        self.bullets.remove(bullet)
                        break
            if bullet.type == 2:
                self.screen.blit(self.bullets.images[bullet.type - 1], (bullet.rect.x - 60, bullet.rect.y))
                self.screen.blit(self.bullets.images[bullet.type - 1], (bullet.rect.x + 60, bullet.rect.y))
                for enemy in self.enemies.enemies:
                    trect = pygame.Rect(enemy.rect.x + self.enemies.x, enemy.rect.y + self.enemies.y, enemy.rect.width, enemy.rect.height)
                    trect2 = Rect(bullet.rect.x-60, bullet.rect.y, bullet.rect.width, bullet.rect.height)
                    if trect.colliderect(trect2):
                        enemy.suffer()
                        self.s_boom.play()
                        collide = True
                    trect2 = Rect(bullet.rect.x+60, bullet.rect.y, bullet.rect.width, bullet.rect.height)
                    if trect.colliderect(trect2):
                        enemy.suffer()
                        self.s_boom.play()
                        collide = True
                if collide:
                    self.bullets.remove(bullet)
                    break
            if bullet.type == 3:
                self.screen.blit(self.bullets.images[bullet.type - 1], (bullet.rect.x - bullet.pos / 2, bullet.rect.y))
                self.screen.blit(self.bullets.images[bullet.type - 1], (bullet.rect.x + bullet.pos / 2, bullet.rect.y))
                for enemy in self.enemies.enemies:
                    trect = pygame.Rect(enemy.rect.x + self.enemies.x, enemy.rect.y + self.enemies.y, enemy.rect.width, enemy.rect.height)
                    trect2 = Rect(bullet.rect.x - bullet.pos / 2, bullet.rect.y, bullet.rect.width, bullet.rect.height)
                    if trect.colliderect(trect2):
                        enemy.suffer()
                        self.s_boom.play()
                        collide = True
                    trect2 = Rect(bullet.rect.x + bullet.pos / 2, bullet.rect.y, bullet.rect.width, bullet.rect.height)
                    if trect.colliderect(trect2):
                        enemy.suffer()
                        self.s_boom.play()
                        collide = True
                if collide:
                    self.bullets.remove(bullet)
                    break
            if bullet.type == 4:
                self.screen.blit(self.bullets.images[bullet.type - 1], (bullet.rect.x + 300 * self.bullets.bullets.index(bullet) / 10 * math.sin(bullet.pos / 100), bullet.rect.y))
                for enemy in self.enemies.enemies:
                    trect = pygame.Rect(enemy.rect.x + self.enemies.x, enemy.rect.y + self.enemies.y, enemy.rect.width, enemy.rect.height)
                    trect2 = Rect(bullet.rect.x + 300 * self.bullets.bullets.index(bullet) / 10 * math.sin(bullet.pos / 100), bullet.rect.y, bullet.rect.width, bullet.rect.height)
                    if trect.colliderect(trect2):
                        enemy.suffer()
                        self.s_boom.play()
                        self.bullets.remove(bullet)
                        break

        for bullet in self.bullets.enemybullets:
            self.screen.blit(self.bullets.images[4], (bullet.rect.x + bullet.pos * math.cos(bullet.angle), bullet.rect.y + bullet.pos * math.sin(bullet.angle)))
            self.screen.blit(self.bullets.images[4], (bullet.rect.x + bullet.pos * math.cos(bullet.angle + math.pi / 3 * 4), bullet.rect.y + bullet.pos * math.sin(bullet.angle + math.pi / 3 * 4)))
            self.screen.blit(self.bullets.images[4], (bullet.rect.x + bullet.pos * math.cos(bullet.angle + math.pi / 3 * 2), bullet.rect.y + bullet.pos * math.sin(bullet.angle + math.pi / 3 * 2)))
            trect = Rect(bullet.rect.x + bullet.pos * math.cos(bullet.angle), bullet.rect.y + bullet.pos * math.sin(bullet.angle), bullet.rect.width, bullet.rect.height)
            if trect.colliderect(self.player.rect):
                self.player.suffer()
                self.s_boom.play()
                self.bullets.removeenemybullet(bullet)
                break
            trect = Rect(bullet.rect.x + bullet.pos * math.cos(bullet.angle + math.pi / 3 * 4), bullet.rect.y + bullet.pos * math.sin(bullet.angle + math.pi / 3 * 4), bullet.rect.width, bullet.rect.height)
            if trect.colliderect(self.player.rect):
                self.player.suffer()
                self.s_boom.play()
                self.bullets.removeenemybullet(bullet)
                break
            trect = Rect(bullet.rect.x + bullet.pos * math.cos(bullet.angle + math.pi / 3 * 2), bullet.rect.y + bullet.pos * math.sin(bullet.angle + math.pi / 3 * 2), bullet.rect.width, bullet.rect.height)
            if trect.colliderect(self.player.rect):
                self.player.suffer()
                self.s_boom.play()
                self.bullets.removeenemybullet(bullet)
                break

        pygame.draw.line(self.screen, (63, 63, 63), [self.player.rect.centerx-100, self.player.rect.centery+100], [self.player.rect.centerx-100+200, self.player.rect.centery+100], 10)
        pygame.draw.line(self.screen, (0, 255, 0), [self.player.rect.centerx-100, self.player.rect.centery+100], [self.player.rect.centerx-100+self.player.life, self.player.rect.centery+100], 10)
        if self.player.suffering < 40:
            self.screen.blit(self.boomsprites[self.player.suffering], (self.player.rect.centerx-75, self.player.rect.centery-73, 150, 145), special_flags = BLEND_ADD)

        for enemy in self.enemies.enemies:
            if enemy.life > 0:
                pygame.draw.line(self.screen, (63, 63, 63), [enemy.rect.centerx - 50 + self.enemies.x, enemy.rect.centery - 75 + self.enemies.y], [enemy.rect.centerx - 50 + 100 + self.enemies.x, enemy.rect.centery - 75 + self.enemies.y], 5)
                pygame.draw.line(self.screen, (255, 0, 0), [enemy.rect.centerx - 50 + self.enemies.x, enemy.rect.centery - 75 + self.enemies.y], [enemy.rect.centerx - 50 + enemy.life + self.enemies.x, enemy.rect.centery - 75 + self.enemies.y], 5)
            if enemy.suffering < 40:
                self.screen.blit(self.boomsprites[enemy.suffering], (enemy.rect.centerx + self.enemies.x - 75, enemy.rect.centery + self.enemies.y -72, 150, 145), special_flags = BLEND_ADD)

        pygame.display.flip()
        self.input(pygame.event.get())
        self.clock.tick(30)


game = Game()
while 1:
    game.step()
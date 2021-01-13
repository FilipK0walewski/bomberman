import pygame
import math


class PlayerMissile:
    def __init__(self, pos, direction):
        self.rect = pygame.Rect(pos[0], pos[1], 8, 8)
        self.direction = direction

        self.img = pygame.image.load('data/assets/sprites/missile.png')
        self.speed = 5

    def update(self):

        if self.direction == 'right':
            self.rect.x += 1 * self.speed
        elif self.direction == 'left':
            self.rect.x -= 1 * self.speed
        elif self.direction == 'down':
            self.rect.y += 1 * self.speed
        elif self.direction == 'up':
            self.rect.y -= 1 * self.speed
        else:
            self.rect.y += 1 * self.speed

    def draw(self, s, display):
        display.blit(self.img, (self.rect.x - s[0], self.rect.y - s[1]))


class Missile:

    def __init__(self, pos, vector, type, angle=0):

        self.type = type
        self.rect = pygame.Rect(pos[0], pos[1], 8, 8)
        self.health = 1000

        self.img = pygame.image.load('data/assets/sprites/missile.png')
        self.axe_img = pygame.image.load('data/assets/sprites/axe.png')

        delta_x = vector[0] - pos[0]
        delta_y = vector[1] - pos[1]
        self.angle = math.atan2(delta_y, delta_x)

        # self.angle = angle * math.pi / 180

        self.speed = 0
        if self.type == 'axe':
            self.speed = 10
        elif self.type == 'bullet':
            self.speed = 3

    def update(self):

        x_move = self.speed * math.cos(self.angle)
        y_move = self.speed * math.sin(self.angle)

        self.rect.x += x_move
        self.rect.y += y_move

    def draw(self, s, display):
        if self.type == 'bullet':
            display.blit(self.img, (self.rect.x - s[0], self.rect.y - s[1]))
        elif self.type == 'axe':

            img = pygame.transform.rotate(self.axe_img, self.angle)
            display.blit(img, (self.rect.x - s[0], self.rect.y - s[1]))
            if self.angle == 0:
                self.angle = 360
            self.angle -= 1

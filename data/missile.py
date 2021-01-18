import pygame
import math


class PlayerMissile:
    def __init__(self, pos, direction):
        self.rect = pygame.Rect(pos[0], pos[1], 8, 8)
        self.direction = direction

        self.img = pygame.image.load('data/assets/sprites/missile.png')
        self.speed = .8
        self.friction = -.01
        self.max_velocity = 5
        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(pos)

    def update(self, dt):

        self.acceleration.x = 0
        self.acceleration.y = 0

        if self.direction == 'right':
            self.acceleration.x += self.speed
        elif self.direction == 'left':
            self.acceleration.x -= self.speed
        elif self.direction == 'up':
            self.acceleration.y -= self.speed
        else:
            self.acceleration.y += self.speed

        self.acceleration += self.velocity * self.friction
        if abs(self.velocity.x) < self.max_velocity:
            self.velocity.x += self.acceleration.x * dt
        if abs(self.velocity.y) < self.max_velocity:
            self.velocity.y += self.acceleration.y * dt

        self.friction -= .002

        self.position += self.velocity * dt + (self.acceleration * .5) * (dt * dt)
        self.rect.x, self.rect.y = self.position

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

        self.friction = -.01
        self.max_velocity = 10
        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(pos)

        self.speed = 0
        if self.type == 'axe':
            self.speed = .1
        elif self.type == 'bullet':
            self.speed = .4

    def update(self, dt):

        x_move = math.cos(self.angle)
        y_move = math.sin(self.angle)

        self.acceleration.x += x_move * .05
        self.acceleration.y += y_move * .05

        if abs(self.velocity.x) < self.max_velocity:
            self.velocity.x += self.acceleration.x * dt
        if abs(self.velocity.y) < self.max_velocity:
            self.velocity.y += self.acceleration.y * dt

        if abs(self.velocity.x) > .1 and abs(self.velocity.y) > .1:
            self.friction -= .001

        self.position += self.velocity * dt + (self.acceleration * .5) * (dt * dt)
        self.rect.x, self.rect.y = self.position

    def draw(self, s, display):
        if self.type == 'bullet':
            display.blit(self.img, (self.rect.x - s[0], self.rect.y - s[1]))
        elif self.type == 'axe':

            img = pygame.transform.rotate(self.axe_img, self.angle)
            display.blit(img, (self.rect.x - s[0], self.rect.y - s[1]))
            if self.angle == 0:
                self.angle = 360
            self.angle -= 1

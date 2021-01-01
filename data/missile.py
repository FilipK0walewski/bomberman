import pygame


class Missile:
    def __init__(self, x, y, direction, flip, type):
        self.x = x
        self.y = y
        self.direction = direction
        self.flip = flip
        self.type = type
        self.missile_rect = pygame.Rect(x, y, 8, 8)
        self.health = 1000

        self.missile_img = pygame.image.load('data/assets/sprites/missile.png')
        self.axe_img = pygame.image.load('data/assets/sprites/axe.png')
        self.angle = 360

        self.speed = 0
        if self.type == 'axe':
            self.speed = 10
        elif self.type == 'bullet':
            self.speed = 10

    def move_missile(self):

        if self.direction == 0:
            self.direction = 'down'
        elif self.direction == 1:
            self.direction = "up"
        elif self.direction == 2:
            if self.flip is True:
                self.direction = 'left'
            else:
                self.direction = 'right'

        if self.direction == 'right':
            self.missile_rect.x += self.speed
        elif self.direction == 'left':
            self.missile_rect.x -= self.speed
        elif self.direction == 'up':
            self.missile_rect.y -= self.speed
        elif self.direction == 'down' or self.direction == 'idle':
            self.missile_rect.y += self.speed

    def draw_missile(self, s, display):
        if self.type == 'bullet':
            display.blit(self.missile_img, (self.missile_rect.x - s[0], self.missile_rect.y - s[1]))
        elif self.type == 'axe':

            img = pygame.transform.rotate(self.axe_img, self.angle)
            display.blit(img, (self.missile_rect.x - s[0], self.missile_rect.y - s[1]))
            if self.angle == 0:
                self.angle = 360
            self.angle -= 1


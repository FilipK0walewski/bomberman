import pygame
from data.images import Spritesheet
import math


class Boss(pygame.sprite.Sprite):
    def __init__(self,  x, y, width, height, player_rect):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = Spritesheet('data/assets/sprites/enemy/boss.png')

        self.friction = -.12
        self.img = sprite_sheet.parse_sprite('boss_0')
        self.rect = self.img.get_rect()
        self.in_cut_scene = True
        self.defeated = False

        self.friction = -.25
        self.position = pygame.math.Vector2(-x / 2, player_rect.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.go_to_pos = pygame.math.Vector2(0, 0)

        self.shoot = False
        self.shoot_tick = 0
        self.last_tick = 0
        self.damage_tick = 0

        self.angle = 0
        self.value = 0

        self.window_w = width / 2
        self.window_h = height / 2
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.max_health = width / 2
        self.health = width / 2
        self.ramka = pygame.Rect(20, self.window_h - 40, self.health - 40, 20)

        self.animation = []
        self.frame = 0
        self.anim_tick = 0
        self.miniature = pygame.image.load('data/assets/sprites/enemy/boss_miniature.png')

        self.rotate_delay = 2500

        for i in range(8):
            temp = 'boss_' + str(i)
            img = sprite_sheet.parse_sprite(temp)
            self.animation.append(img)

    def draw_boss(self, scroll, display):

        tick = pygame.time.get_ticks()
        if tick - self.anim_tick > 25:
            self.anim_tick = tick
            self.frame = (self.frame + 1) % len(self.animation)

        display.blit(pygame.transform.rotate(self.animation[self.frame], self.angle), (self.rect.x - scroll.x, self.rect.y - scroll.y))

    def draw_health_bar(self, display):
        health_bar = pygame.Rect(20, self.window_h - 40, self.health - 40, 20)
        pygame.draw.rect(display, self.red, health_bar)
        pygame.draw.rect(display, self.black, self.ramka, 2)
        display.blit(self.miniature, (8, self.window_h - 45))

    def update(self, map_rect, player_rect, dt):

        self.acceleration.x = 0
        self.acceleration.y = 0

        if self.in_cut_scene is True:
            self.rotate_delay = 0
        else:
            pass
            # self.rotate_delay = 2500

        if self.max_health < self.health * 2:
            self.value = 25
            tick = pygame.time.get_ticks()
            if tick - self.last_tick > self.rotate_delay:
                self.rotate_delay -= 100
                self.last_tick = tick

                self.go_to_pos.x = player_rect[0]
                self.go_to_pos.y = player_rect[1]

                delta = self.go_to_pos - self.position

                radians = math.atan2(-delta[1], delta[0])
                self.angle = (radians * 180) / math.pi - 90

            if tick - self.shoot_tick > 500:
                self.shoot_tick = tick
                self.shoot = True

        elif self.max_health > self.health * 2:
            self.value = 50
            if self.position.x >= 2 * self.window_w:
                self.go_to_pos.y = player_rect[1]
                self.go_to_pos.x = -self.window_w * 2
                self.angle = 90
            elif self.position.x <= -self.window_w:
                self.go_to_pos.y = player_rect[1]
                self.go_to_pos.x = 3 * self.window_w
                self.angle = 270

        if self.position != self.go_to_pos:
            # self.acceleration.x += 50
            # self.acceleration.y += 50
            self.acceleration.x += (self.go_to_pos.x - self.position.x) / self.value
            self.acceleration.y += (self.go_to_pos.y - self.position.y) / self.value
        # self.acceleration *= 2

        self.acceleration.x += self.velocity.x * self.friction
        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(2)
        if self.in_cut_scene is False:
            self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
            self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.center = self.position

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0
        if abs(self.velocity.y) < .01:
            self.velocity.y = 0

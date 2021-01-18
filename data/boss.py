import pygame
from data.images import Spritesheet
import math


class Boss(pygame.sprite.Sprite):
    def __init__(self,  x, width, height, player_rect):
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = Spritesheet('data/assets/sprites/enemy/boss.png')

        self.friction = -.12
        self.img = sprite_sheet.parse_sprite('boss_0')
        self.rect = self.img.get_rect()
        self.in_cut_scene = True
        self.defeated = False
        self.radius = 360
        self.img_color = (255, 255, 255)

        self.position = pygame.math.Vector2(-x / 2, player_rect.y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.vector = pygame.math.Vector2(0, 0)

        self.shoot = False
        self.shoot_tick = 0
        self.last_tick = 0
        self.damage_tick = 0

        self.angle = 0

        self.window_w = width / 2
        self.window_h = height / 2
        self.padding = self.window_w * .05
        self.red = (255, 0, 16)
        self.black = (0, 0, 0)
        self.max_health = 1000
        self.current_health = 1000

        self.health_bar = pygame.Rect(self.padding, self.window_h - 2 * self.padding, self.window_w * .9, self.padding * .5)
        self.health_width = self.health_bar.width
        self.ramka = pygame.Rect(self.padding, self.window_h - 2 * self.padding, self.window_w * .9, self.padding * .5)

        self.animation = []
        self.frame = 0
        self.anim_tick = 0
        self.miniature = pygame.image.load('data/assets/sprites/enemy/boss_miniature.png')
        self.miniature_pos = list(self.ramka.topleft)
        self.miniature_pos[0] -= self.miniature.get_width() / 2

        self.rotate_delay = 2500

        for i in range(8):
            temp = 'boss_' + str(i)
            img = sprite_sheet.parse_sprite(temp)
            self.animation.append(img)

    def draw_boss(self, scroll, display):

        img = self.animation[self.frame]

        temp = pygame.Surface(img.get_size())
        temp.fill(self.img_color)

        output_image = img.copy()
        output_image.blit(temp, (0, 0), special_flags=pygame.BLEND_MULT)

        tick = pygame.time.get_ticks()
        if tick - self.anim_tick > 25:
            self.anim_tick = tick
            self.frame = (self.frame + 1) % len(self.animation)
        if abs(self.velocity.x) < .1 and abs(self.velocity.y) < .1:
            self.frame = 0

        if self.defeated is False:
            display.blit(pygame.transform.rotate(output_image, self.angle), (self.rect.x - scroll.x, self.rect.y - scroll.y))

    def draw_health_bar(self, display):
        pygame.draw.rect(display, self.red, self.health_bar, border_radius=5)
        pygame.draw.rect(display, self.black, self.ramka, 2, border_radius=5)

        display.blit(self.miniature, self.miniature_pos)

    def update(self, player_rect, bomb_rect, dt):

        self.acceleration.x = 0
        self.acceleration.y = 0

        tick = pygame.time.get_ticks()
        if tick - self.shoot_tick > 1500:
            self.shoot_tick = tick
            self.shoot = True

        if self.max_health > self.current_health * 2:
            delta_x = player_rect[0] - self.position.x
            delta_y = player_rect[1] - self.position.y

            radius = delta_y**2 + delta_x**2

            if math.sqrt(radius) > self.radius:

                radians = math.atan2(delta_y, delta_x)

                self.vector.x = math.cos(radians)
                self.vector.y = math.sin(radians)

                self.angle = -(radians * 180) / math.pi - 90

        else:
            line = ()
            for rect in bomb_rect:
                line = rect.clipline(self.position, (player_rect[0], player_rect[1]))

            if len(line) != 0:
                for li in line:
                    if li[0] < self.position.x:
                        delta_x = li[0] + 96 - self.position.x
                    else:
                        delta_x = li[0] - 96 - self.position.x
                    if li[1] < self.position.y:
                        delta_y = li[1] + 96 - self.position.y
                    else:
                        delta_y = li[1] - 96 - self.position.y
            else:
                delta_x = player_rect[0] - self.position.x
                delta_y = player_rect[1] - self.position.y

            radians = math.atan2(delta_y, delta_x)

            self.vector.x = math.cos(radians) * .15
            self.vector.y = math.sin(radians) * .15

            p_x = player_rect[0] - self.position.x
            p_y = player_rect[1] - self.position.y
            rotation_radians = math.atan2(p_y, p_x)

            self.angle = -(rotation_radians * 180) / math.pi - 90

        self.acceleration += self.vector

        self.acceleration += self.velocity * self.friction
        self.velocity += self.acceleration * dt

        if self.in_cut_scene is False:
            self.position += self.velocity * dt + (self.acceleration * .5) * (dt * dt)

        self.rect.center = self.position

    def take_damage(self, damage):
        tick = pygame.time.get_ticks()
        if tick - 500 > self.damage_tick:
            self.current_health -= damage
            percent = self.current_health / self.max_health
            self.health_bar.width = self.health_width * percent
            self.damage_tick = tick

import pygame
from data.images import Spritesheet


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        x_start = 232
        y_start = 256
        self.rect = pygame.Rect(x_start, y_start, 16, 16)
        self.left_key, self.right_key, self.up_key, self.down_key = False, False, False, False

        # new

        self.friction = -.25
        self.position = pygame.math.Vector2(x_start, y_start)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

        # old

        self.player_hearts = 3
        self.frame = 0

        self.action = 'idle'
        self.direction = self.action
        self.last_tick = 0
        self.player_stuck = False

        self.on_bomb = False
        self.bomb_number = 1
        self.coins = 0
        self.temp = 0

        self.animation_left = []
        self.animation_right = []
        self.animation_up = []
        self.animation_down = []
        self.load_images()
        self.img = self.animation_down[0]

    def load_images(self):
        spritesheet = Spritesheet('data/assets/sprites/spritesheet.png')
        for n in range(8):
            path_r = 'player_side_' + str(n)
            path_d = 'player_down_' + str(n)
            path_u = 'player_up_' + str(n)

            image_r = spritesheet.parse_sprite(path_r)
            image_d = spritesheet.parse_sprite(path_d)
            image_u = spritesheet.parse_sprite(path_u)
            self.animation_right.append(image_r)
            self.animation_down.append(image_d)
            self.animation_up.append(image_u)
            self.animation_left.append(pygame.transform.flip(image_r, True, False))

    def draw_player(self, s, display):
        display.blit(self.img, (self.rect.x - 8 - s. x, self.rect.y - 16 - s.y))

    def move_player(self, map_rect, dt):
        self.acceleration.x = 0
        self.acceleration.y = 0
        self.player_stuck = False

        if self.left_key:
            self.acceleration.x -= .5
            self.action = 'left'
        if self.right_key:
            self.acceleration.x += .5
            self.action = 'right'
        if self.down_key:
            self.acceleration.y += .5
            self.action = 'down'
        if self.up_key:
            self.acceleration.y -= .5
            self.action = 'up'

        if self.acceleration.x == 0 and self.acceleration.y == 0:
            self.action = 'idle'
        else:
            self.direction = self.action

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(20)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.rect.w
                self.rect.x = self.position.x
                if self.action == 'right':
                    self.player_stuck = True
            elif self.velocity.x < 0:
                self.position.x = tile.right
                self.rect.x = self.position.x
                if self.action == 'left':
                    self.player_stuck = True

        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(20)
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.y = self.position.y

        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.velocity.y > 0:
                self.position.y = tile.top - self.rect.h
                self.rect.y = self.position.y
                if self.action == 'down':
                    self.player_stuck = True
            elif self.velocity.y < 0:
                self.position.y = tile.bottom
                self.rect.y = self.position.y
                if self.action == 'up':
                    self.player_stuck = True

        self.animate()

    def animate(self):
        tick = pygame.time.get_ticks()
        if self.action == 'idle' or self.player_stuck is True:
            if self.direction == 'left':
                self.img = self.animation_left[0]
            elif self.direction == 'right':
                self.img = self.animation_right[0]
            elif self.direction == 'down':
                self.img = self.animation_down[0]
            elif self.direction == 'up':
                self.img = self.animation_up[0]

        else:
            if tick - self.last_tick > 75:
                self.last_tick = tick
                self.frame = (self.frame + 1) % len(self.animation_down)

            if self.action == 'left':
                self.img = self.animation_left[self.frame]
            elif self.action == 'right':
                self.img = self.animation_right[self.frame]
            elif self.action == 'down':
                self.img = self.animation_down[self.frame]
            elif self.action == 'up':
                self.img = self.animation_up[self.frame]

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def collision_test(self, map_rect):
        hit_list = []
        for tile in map_rect:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

import random
import pygame


class Enemy:

    def __init__(self, spawn_rect, display, speed=1):
        n = len(spawn_rect)
        r = spawn_rect[random.randint(0, n)]

        self.spawn_rect = spawn_rect
        self.turn_rect = []
        self.display = display
        self.enemy_rect = pygame.Rect(r.x, r.y, 32, 32)
        self.speed = speed
        self.movement = [0, 0]
        self.enemy_hp = 20
        self.enemy_img = 0
        self.directions = {'right', 'left', 'up', 'down'}
        self.start = True
        self.direction = 'right'

    def load_image(self):
        self.enemy_img = pygame.image.load('assets/sprites/enemy_0.png')
        self.find_place_to_turn()

    def draw_enemy(self, scroll):
        hit_box = (self.enemy_rect.x, self.enemy_rect.y, 32, 32)
        self.display.blit(self.enemy_img, (self.enemy_rect.x - scroll[0], self.enemy_rect.y - scroll[1]))
        pygame.draw.rect(self.display, (255, 0, 0), (hit_box[0] - scroll[0], hit_box[1] - scroll[1],
                                                     hit_box[2], hit_box[3]), 2)

    def move_enemy(self, map_rect, bomb_rect):

        if self.start is True:
            self.direction = random.choice(list(self.directions))
            self.start = False

        if self.direction == 'right':
            self.movement[0] = 1
        elif self.direction == 'left':
            self.movement[0] = -1
        elif self.direction == 'up':
            self.movement[1] = -1
        elif self.direction == 'down':
            self.movement[1] = 1

        self.enemy_rect.x += self.movement[0]
        self.enemy_rect.y += self.movement[1]

        for tile in self.turn_rect:
            if tile[0] == self.enemy_rect.x and tile[1] == self.enemy_rect.y:
                self.direction = random.choice(list(self.directions))

        self.bomb_collider(bomb_rect)

        for tile in map_rect:
            if self.enemy_rect.colliderect(tile):
                if self.movement[0] > 0:
                    self.enemy_rect.right = tile.left
                if self.movement[0] < 0:
                    self.enemy_rect.left = tile.right
                if self.movement[1] > 0:
                    self.enemy_rect.bottom = tile.top
                if self.movement[1] < 0:
                    self.enemy_rect.top = tile.bottom
                self.direction = random.choice(list(self.directions))

        self.set_movement(0, 0)

    def find_player(self, player_rect):
        if player_rect.x < self.enemy_rect.x:
            if player_rect.y < self.enemy_rect.y:
                self.set_movement(-1, -1)
            if player_rect.y > self.enemy_rect.y:
                self.set_movement(-1, 2)
            if player_rect.y == self.enemy_rect.y:
                self.set_movement(-1, 0)
        if player_rect.x > self.enemy_rect.x:
            if player_rect.y < self.enemy_rect.y:
                self.set_movement(2, -1)
            if player_rect.y > self.enemy_rect.y:
                self.set_movement(2, 2)
            if player_rect.y == self.enemy_rect.y:
                self.set_movement(2, 0)
        if player_rect.x == self.enemy_rect.x:
            if player_rect.y < self.enemy_rect.y:
                self.set_movement(0, -1)
            if player_rect.y > self.enemy_rect.y:
                self.set_movement(0, 2)

    def find_place_to_turn(self):
        temp_list = []
        for tile in self.spawn_rect:
            temp_tile = list(tile)
            temp_list.append(temp_tile)

        for tile in temp_list:
            temp_tile_l = tile.copy()
            temp_tile_r = tile.copy()
            temp_tile_u = tile.copy()
            temp_tile_d = tile.copy()
            temp_tile_l[0] = temp_tile_l[0] - 32
            temp_tile_r[0] = temp_tile_r[0] + 32
            temp_tile_u[1] = temp_tile_l[1] - 32
            temp_tile_d[1] = temp_tile_r[1] + 32

            if temp_tile_r in temp_list and temp_tile_l in temp_list\
                    and temp_tile_u in temp_list and temp_tile_d in temp_list:
                self.turn_rect.append(tile)

    def set_movement(self, x, y):
        self.movement = [x, y]

    def get_hp(self):
        return self.enemy_hp

    def take_damage(self, damage):
        self.enemy_hp -= damage

    def get_rect(self):
        return self.enemy_rect

    def bomb_collider(self, bomb_rect):
        for tile in bomb_rect:
            if self.enemy_rect.colliderect(tile):
                if self.movement[0] > 0:
                    self.enemy_rect.right = tile.left
                if self.movement[0] < 0:
                    self.enemy_rect.left = tile.right
                if self.movement[1] > 0:
                    self.enemy_rect.bottom = tile.top
                if self.movement[1] < 0:
                    self.enemy_rect.top = tile.bottom
                self.direction = random.choice(list(self.directions))


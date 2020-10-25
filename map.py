import random
import pygame


class Map:

    def __init__(self, display, level):
        self.display = display
        self.door_spawned = False
        self.door_opened = False
        self.door_rect = pygame.Rect
        self.tile_size = 32

        self.spawn_rect = []
        self.map_rect = []
        self.game_map = []
        self.hard_wall = []
        self.bomb_coin_rect = []
        self.explosion_coin_rect = []

        self.grass = []
        self.rock_img = pygame.image.load('assets/sprites/rocks/rock_0.png')
        self.tree_img = pygame.image.load('assets/sprites/tree_0.png')
        self.door_img = pygame.image.load('assets/sprites/door.png')
        self.door_closed_img = pygame.image.load('assets/sprites/door_closed.png')
        self.hard_wall_img = pygame.image.load('assets/sprites/hard_wall.png')
        self.bomb_coin = pygame.image.load('assets/sprites/bomb_add.png')
        self.explosion_coin = pygame.image.load('assets/sprites/explosion_add.png')

        self.load_images()
        self.level = level
        self.load_map('assets/maps/map_' + str(self.level) + '.txt')

    def load_images(self):

        for n in range(4):
            img = pygame.image.load('assets/sprites/grass/grass_' + str(n) + '.png')
            self.grass.append(img)

    def display_map(self, s):

        n = int(0)
        for layer in self.game_map:
            m = int(0)
            for tile in layer:
                self.display.blit(self.grass[0], (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                if tile == '1':
                    self.display.blit(self.rock_img, (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                if tile == '2':
                    self.display.blit(self.tree_img, (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                if tile == '3':
                    self.display.blit(self.grass[0], (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                    self.display.blit(self.bomb_coin, (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                if tile == '4':
                    self.display.blit(self.grass[0], (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                    self.display.blit(self.explosion_coin, (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                if tile == '5':
                    if self.door_opened is True:
                        self.display.blit(self.door_img, (m * self.tile_size - s[0], n * self.tile_size - s[1]))
                    else:
                        self.display.blit(self.door_closed_img, (m * self.tile_size - s[0], n * self.tile_size - s[1]))

                if tile == '1' or tile == '2':
                    self.map_rect.append(pygame.Rect(m * self.tile_size,
                                                     n * self.tile_size, self.tile_size, self.tile_size))
                m += 1
            n += 1

    def load_map(self, path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = data.split('\n')

        for row in data:
            self.game_map.append(list(row))

        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                temp_tuple = (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if tile == '0':
                    if random.randint(1, 3) == 1:
                        self.game_map[y][x] = '2'
                    else:
                        self.spawn_rect.append(pygame.Rect(temp_tuple))
                if tile == '1':
                    self.hard_wall.append(pygame.Rect(temp_tuple))

                x += 1
            y += 1

    def wall_destroying(self, explosion_rect):

        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                temp_tuple = (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if tile == '2':
                    for i in range(len(explosion_rect)):
                        if pygame.Rect(temp_tuple).colliderect(explosion_rect[i]):
                            n = random.randint(1, 10)
                            if n == 1:
                                self.game_map[y][x] = '3'
                                self.bomb_coin_rect.append(temp_tuple)
                            elif n == 2:
                                self.game_map[y][x] = '4'
                                self.explosion_coin_rect.append(temp_tuple)
                            elif n == 3:
                                if self.door_spawned is False:
                                    self.game_map[y][x] = '5'
                                    self.door_rect = pygame.Rect(temp_tuple)
                                    self.door_spawned = True
                                else:
                                    self.game_map[y][x] = '0'
                            else:
                                self.game_map[y][x] = '0'
                x += 1
            y += 1

    def get_tile_rect(self):
        return self.map_rect

    def tile_map_reset(self):
        self.map_rect = []

    def get_spawn_rect(self):
        return self.spawn_rect

    def get_door_rect(self):
        return self.door_rect

    def check_door(self):
        return self.door_opened

    def open_the_door(self):
        self.door_opened = True

    def reset(self):
        self.spawn_rect = []
        self.map_rect = []
        self.game_map = []

    def get_hard_wall(self):
        return self.hard_wall

    def get_bomb_coin_rect(self):
        return self.bomb_coin_rect

    def get_explosion_coin_rect(self):
        return self.explosion_coin_rect

    def coin_picking(self, coin_rect, coin_type):
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                print(tile)
                temp_tuple = (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if temp_tuple == coin_rect:
                    self.game_map[y][x] = '0'
                x += 1
            y += 1

        if coin_type == 'bomb':
            self.bomb_coin_rect.remove(coin_rect)

        if coin_type == 'explosion':
            self.explosion_coin_rect.remove(coin_rect)

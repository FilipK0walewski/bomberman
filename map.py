import random
import pygame


class Map:

    def __init__(self, display, door=False):
        self.display = display
        self.door = door
        self.door_rect = 0
        self.tile_size = 32

        self.spawn_rect = []
        self.map_rect = []
        self.game_map = []
        self.grass = []
        self.rock_img = 0
        self.tree_img = 0
        self.door_img = 0
        self.hard_wall_img = 0

    def load_images(self):

        for n in range(4):
            img = pygame.image.load('assets/sprites/grass/grass_' + str(n) + '.png')
            self.grass.append(img)

        self.rock_img = pygame.image.load('assets/sprites/rocks/rock_0.png')
        self.tree_img = pygame.image.load('assets/sprites/tree_0.png')
        self.door_img = pygame.image.load('assets/sprites/door.png')
        self.hard_wall_img = pygame.image.load('assets/sprites/hard_wall.png')

    def display_map(self, s):

        y = int(0)
        for layer in self.game_map:
            x = int(0)
            for tile in layer:
                if tile == '1':
                    self.display.blit(self.rock_img, (x * self.tile_size - s[0], y * self.tile_size - s[1]))
                if tile == '2':
                    self.display.blit(self.tree_img, (x * self.tile_size - s[0], y * self.tile_size - s[1]))
                if tile == '0':
                    self.display.blit(self.grass[0], (x * self.tile_size - s[0], y * self.tile_size - s[1]))

                if tile != '0':
                    self.map_rect.append(pygame.Rect(x * self.tile_size,
                                                     y * self.tile_size, self.tile_size, self.tile_size))
                if self.door is True:
                    if self.tile_size * x == self.door_rect.x and self.tile_size * y == self.door_rect.y:
                        self.display.blit(self.door_img, (x * self.tile_size - s[0], y * self.tile_size - s[1]))

                x += 1
            y += 1

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
                """
                if tile == '1':
                    self.game_map[y][x] = str(random.randint(1, 2))
                    """
                if tile == '0':
                    if random.randint(1, 10) == 1:
                        self.game_map[y][x] = '2'
                    else:
                        self.spawn_rect.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size,
                                                           self.tile_size))
                x += 1

            y += 1

    def wall_destroying(self, explosion_rect):

        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile == '2':
                    for i in range(len(explosion_rect)):
                        if pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size,
                                            self.tile_size).colliderect(explosion_rect[i]):
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

    def spawn_door(self):
        self.door = True
        n = random.randint(0, len(self.spawn_rect))
        self.door_rect = pygame.Rect(self.spawn_rect[n].x, self.spawn_rect[n].y, 32, 32)

        print("door: ", self.door_rect.x, " ", self.door_rect.y)

    def remove_door(self):
        self.door = False

    def check_door(self):
        return self.door

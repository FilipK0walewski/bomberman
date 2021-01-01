import pygame
from data.images import Spritesheet


class Bomb:

    def __init__(self, bomb_rect, hard_wall, soft_wall, explosion_length):
        self.bomb_rect = pygame.Rect(bomb_rect.x, bomb_rect.y, 32, 32)
        self.hard_wall = hard_wall
        self.soft_wall = soft_wall

        self.explosion_rect = []
        self.explosion_length = explosion_length
        self.frame = 0
        self.explosion_frame = 0
        self.value = 1

        self.x_edges = []
        self.y_edges = []
        self.bomb_sheet = Spritesheet('data/assets/sprites/spritesheet.png')
        self.explosion_sheet = Spritesheet('data/assets/sprites/explosion/explosion.png')
        self.help_variable = 0

    def draw_bomb(self, s, display, image):
        if not self.explosion_rect:
            display.blit(image[self.frame], (self.bomb_rect.x - s[0], self.bomb_rect.y - s[1]))
            self.frame += 1
            if self.frame == len(image):
                self.frame -= 1

    def find_edges(self):
        self.x_edges = []
        self.y_edges = []
        temp_max_y, temp_max_x, temp_min_y, temp_min_x = 0, 0, 1000000, 1000000
        for tile in self.explosion_rect:
            if tile.x > temp_max_x:
                temp_max_x = tile.x
            if tile.y > temp_max_y:
                temp_max_y = tile.y
            if tile.y < temp_min_y:
                temp_min_y = tile.y
            if tile.x < temp_min_x:
                temp_min_x = tile.x

        self.x_edges.append(temp_max_x)
        self.x_edges.append(temp_min_x)
        self.y_edges.append(temp_max_y)
        self.y_edges.append(temp_min_y)

    def draw_explosion(self, s, display):
        if self.explosion_rect:
            for tile in self.explosion_rect:

                if tile.x == self.bomb_rect.x and tile.y == self.bomb_rect.y:
                    name = "center_" + str(self.explosion_frame) + ".png"
                    image = self.explosion_sheet.parse_sprite(name)
                else:
                    if tile.x in self.x_edges and tile.y == self.bomb_rect.y or tile.y in self.y_edges and tile.x == self.bomb_rect.x:
                        name = "edge_" + str(self.explosion_frame) + ".png"
                        image = self.explosion_sheet.parse_sprite(name)
                    else:
                        name = "middle_" + str(self.explosion_frame) + ".png"
                        image = self.explosion_sheet.parse_sprite(name)

                    if tile.y < self.bomb_rect.y:
                        image = pygame.transform.rotate(image, 90)
                    elif tile.y > self.bomb_rect.y:
                        image = pygame.transform.rotate(image, 270)
                    elif tile.x < self.bomb_rect.x:
                        image = pygame.transform.rotate(image, 180)

                display.blit(image, (tile.x - s[0], tile.y - s[1]))

            if self.frame % 3 == 0:
                self.explosion_frame += self.value
            self.frame += 1

            if self.explosion_frame == 7:
                self.value = self.value * (-1)
                self.explosion_frame += self.value
            if self.explosion_frame == 0 and self.value < 0:
                self.value = self.value * (-1)

    def collision_test(self, hit_box):
        hit_list = []

        for tile in hit_box:
            if self.bomb_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_bomb(self, hit_box):

        self.bomb_position_correction()
        hit_list = self.collision_test(hit_box)

        for tile in hit_list:
            if self.bomb_rect.x < tile.x:
                self.bomb_rect.right = tile.left
            elif self.bomb_rect.y < tile.y:
                self.bomb_rect.bottom = tile.top
            elif self.bomb_rect.x > tile.x:
                self.bomb_rect.left = tile.right
            elif self.bomb_rect.y > tile.y:
                self.bomb_rect.top = tile.bottom

    def bomb_position_correction(self):
        if self.bomb_rect.x % 16 >= 16:
            self.bomb_rect.x += (32 - self.bomb_rect.x % 32)
        else:
            self.bomb_rect.x -= self.bomb_rect.x % 32

        if self.bomb_rect.y % 16 >= 16:
            self.bomb_rect.y += (32 - self.bomb_rect.y % 32)
        else:
            self.bomb_rect.y -= self.bomb_rect.y % 32

    def explosion(self):
        self.explosion_rect = []
        temp_tuple = (self.bomb_rect.x, self.bomb_rect.y, 32, 32)
        self.explosion_rect.append(pygame.Rect(temp_tuple))

        temp_list = [False, False, False, False]

        for n in range(self.explosion_length + 1):
            temp_dict = {(self.bomb_rect.x + (n * 32), self.bomb_rect.y, 32, 32): temp_list[0],
                         (self.bomb_rect.x - (n * 32), self.bomb_rect.y, 32, 32): temp_list[1],
                         (self.bomb_rect.x, self.bomb_rect.y + (n * 32), 32, 32): temp_list[2],
                         (self.bomb_rect.x, self.bomb_rect.y - (n * 32), 32, 32): temp_list[3]}
            x = 0
            for m, o in temp_dict.items():
                temp_rect = pygame.Rect(m)
                wall_found = o
                if wall_found is False:
                    for wall in self.hard_wall:
                        if wall.colliderect(temp_rect):
                            temp_list[x] = True
                            wall_found = True
                            break
                    for wall in self.soft_wall:
                        if wall.colliderect(temp_rect):
                            temp_list[x] = True
                            wall_found = True
                            self.explosion_rect.append(temp_rect)
                            break
                    if wall_found is False:
                        self.explosion_rect.append(temp_rect)
                x += 1

    def bomb_falling(self, display, img):
        self.bomb_rect.y += 1
        display.blit(img, (self.bomb_rect.x, self.bomb_rect.y))

import pygame


class Bomb:

    def __init__(self, bomb_rect, display, hard_wall, explosion_lenth):
        self.display = display
        self.bomb_rect = pygame.Rect(bomb_rect.x, bomb_rect.y, 32, 32)
        self.hard_wall = hard_wall

        self.explosion_rect = []
        self.bomb = []
        self.explosion_frames = []
        self.explosion_length = explosion_lenth
        self.frame = 0
        self.bomb_exploded = False
        self.load_images()

    def load_images(self):
        for n in range(5):
            for m in range(36):
                img = pygame.image.load('assets/sprites/bomb/bomb_' + str(n) + '.png')
                self.bomb.append(img)

        for n in range(7):
            for m in range(10):
                img = pygame.image.load('assets/sprites/explosion/explosion_' + str(n) + '.png')
                self.explosion_frames.append(img)

    def draw_bomb(self, s):
        self.explosion_rect = []
        if self.bomb_exploded is False:
            self.display.blit(self.bomb[self.frame], (self.bomb_rect.x - s[0], self.bomb_rect.y - s[1]))
            self.frame += 1

            if int(self.frame) == int(len(self.bomb)):
                self.frame = 0
                self.bomb_exploded = True

    def draw_explosion(self, s):
        if self.bomb_exploded is True:
            for tile in self.explosion_rect:
                self.display.blit(self.explosion_frames[self.frame], (tile.x - s[0], tile.y - s[1]))
            self.frame += 1

    def collision_test(self, hit_box):
        hit_list = []

        for tile in hit_box:
            if self.bomb_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_bomb(self, hit_box):

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

    def explosion(self):

        temp_tuple = (self.bomb_rect.x, self.bomb_rect.y, 32, 32)
        self.explosion_rect.append(pygame.Rect(temp_tuple))

        for n in range(self.explosion_length + 1):
            self.explosion_rect.append(pygame.Rect(self.bomb_rect.x + (n * 32), self.bomb_rect.y, 32, 32))
            self.explosion_rect.append(pygame.Rect(self.bomb_rect.x - (n * 32), self.bomb_rect.y, 32, 32))
            self.explosion_rect.append(pygame.Rect(self.bomb_rect.x, self.bomb_rect.y + (n * 32), 32, 32))
            self.explosion_rect.append(pygame.Rect(self.bomb_rect.x, self.bomb_rect.y - (n * 32), 32, 32))

        for wall in self.hard_wall:
            for e_tile in self.explosion_rect:
                if wall.colliderect(e_tile):
                    self.explosion_rect.remove(e_tile)

    def get_explosion_rect(self):
        return self.explosion_rect

    def bigger_explosion_length(self):
        self.explosion_length =+ 1

    def get_bomb_rect(self):
        return self.bomb_rect

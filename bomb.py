import pygame


class Bomb:

    def __init__(self, bomb_rect, display):
        self.display = display
        self.bomb_rect = pygame.Rect(bomb_rect.x, bomb_rect.y, 32, 32)
        self.explosion_rect = []
        self.bomb = []
        self.frame = 0

    def load_images(self):
        for n in range(5):
            for m in range(20):
                img = pygame.image.load('assets/sprites/bomb/bomb_' + str(n) + '.png')
                self.bomb.append(img)

        for n in range(7):
            for m in range(20):
                img = pygame.image.load('assets/sprites/explosion/explosion_' + str(n) + '.png')
                self.bomb.append(img)

    def draw_bomb(self, s):
        self.display.blit(self.bomb[self.frame], (self.bomb_rect.x - s[0], self.bomb_rect.y - s[1]))

        if self.frame < len(self.bomb):
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
        self.explosion_rect.append(pygame.Rect(self.bomb_rect.x, self.bomb_rect.y, 32, 32))
        self.explosion_rect.append(pygame.Rect(self.bomb_rect.x + 32, self.bomb_rect.y + 8, 16, 16))
        self.explosion_rect.append(pygame.Rect(self.bomb_rect.x - 16, self.bomb_rect.y + 8, 16, 16))
        self.explosion_rect.append(pygame.Rect(self.bomb_rect.x + 8, self.bomb_rect.y + 32, 16, 16))
        self.explosion_rect.append(pygame.Rect(self.bomb_rect.x + 8, self.bomb_rect.y - 16, 16, 16))

    def get_explosion_rect(self):
        return self.explosion_rect

    def get_bomb_rect(self):
        return self.bomb_rect

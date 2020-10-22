import random
import pygame


class Player:

    def __init__(self, wx, wy, display, spawn):
        self.player_size = 32

        self.x = wx / 2 - self.player_size / 2
        self.y = wy / 2 - self.player_size / 2

        r = spawn[random.randint(0, len(spawn))]
        rx = r.x
        ry = r.y

        self.display = display
        self.player_rect = pygame.Rect(rx, ry, 32, 32)

        self.player_hp = int(100)
        self.player_movement = [0, 0]
        self.player_size = 32
        self.player_speed = 2

        self.frame = 0
        self.frames_per_image = 3
        self.player_actions = {'right', 'up', 'down', 'idle'}
        self.flip = False
        self.action = 'idle'
        self.animations = {}

        self.true_scroll = [0, 0]

    def load_images(self):

        for action in self.player_actions:
            temp_list = []
            for n in range(8):
                for m in range(self.frames_per_image):

                    if action == 'idle' and n > 3:
                        n = 0

                    img = pygame.image.load('assets/sprites/player/player_' + str(action) + '_' + str(n) + '.png')
                    temp_list.append(img)

            self.animations[action] = temp_list

    def draw_player(self, s):
        player_img = self.animations[self.action][self.frame]
        self.frame += 1
        if self.frame == len(self.animations[self.action]):
            self.frame = 0

        self.display.blit(player_img, (self.player_rect.x - s[0], self.player_rect.y - s[1]))
        self.display.blit(pygame.transform.flip(player_img, self.flip, False),
                          (self.player_rect.x - s[0], self.player_rect.y - s[1]))

    def collision_test(self, map_rect):
        hit_list = []
        for tile in map_rect:
            if self.player_rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move_player(self, map_rect):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.player_movement[0] -= 1 * self.player_speed
            self.flip = True
            self.action = 'right'
        if keys[pygame.K_RIGHT]:
            self.player_movement[0] += 1 * self.player_speed
            self.flip = False
            self.action = 'right'
        if keys[pygame.K_DOWN]:
            self.player_movement[1] += 1 * self.player_speed
            self.action = 'down'
        if keys[pygame.K_UP]:
            self.player_movement[1] -= 1 * self.player_speed
            self.action = 'up'
        if self.player_movement == [0, 0]:
            self.action = 'idle'

        self.player_rect.x += self.player_movement[0]
        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.player_movement[0] > 0:
                self.player_rect.right = tile.left
            elif self.player_movement[0] < 0:
                self.player_rect.left = tile.right

        self.player_rect.y += self.player_movement[1]
        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.player_movement[1] > 0:
                self.player_rect.bottom = tile.top
            elif self.player_movement[1] < 0:
                self.player_rect.top = tile.bottom

        self.player_movement_reset()

    def player_movement_reset(self):
        self.player_movement = [0, 0]

    def get_player_rect(self):
        return self.player_rect

    def scroll(self):

        self.true_scroll[0] += (self.player_rect.x - self.true_scroll[0] - self.x) / 5
        self.true_scroll[1] += (self.player_rect.y - self.true_scroll[1] - self.y) / 5
        scroll = self.true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        return scroll

    def set_player_hp(self, value):
        self.player_hp += value

    def get_player_hp(self):
        return self.player_hp

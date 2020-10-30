import random
import pygame


class Player:

    def __init__(self, wx, wy, spawn):
        self.player_size = 32

        self.x = (wx / 2 - self.player_size / 2) / 2
        self.y = (wy / 2 - self.player_size / 2) / 2

        self.x_start = 32
        self.y_start = 32

        """
        r = spawn[random.randint(0, len(spawn))]
        rx = r.x
        ry = r.y
        """

        self.player_rect = pygame.Rect(self.x_start, self.y_start, 32, 32)

        self.player_hearts = 3
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
        self.on_bomb = False

        self.bomb_number = 1
        self.load_images()

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

    def draw_player(self, s, display):
        player_img = self.animations[self.action][self.frame]
        self.frame += 1
        if self.frame == len(self.animations[self.action]):
            self.frame = 0

        display.blit(player_img, (self.player_rect.x - s[0], self.player_rect.y - s[1]))
        display.blit(pygame.transform.flip(player_img, self.flip, False),
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
        if keys[pygame.K_SPACE]:
            pass

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

        # self.bomb_collider(bomb_rect)

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

    def bomb_collider(self, bomb_rect):

        for tile in bomb_rect:
            if self.on_bomb is True:
                if self.player_rect.colliderect(tile):
                    pass
                else:
                    self.on_bomb = False
            else:
                print("not on bomb")
                if self.player_rect.colliderect(tile):
                    if self.player_movement[0] > 0:
                        self.player_rect.right = tile.left
                    if self.player_movement[0] < 0:
                        self.player_rect.left = tile.right
                    if self.player_movement[1] > 0:
                        self.player_rect.bottom = tile.top
                    if self.player_movement[1] < 0:
                        self.player_rect.top = tile.bottom

    def add_bomb(self):
        self.bomb_number += 1

    def remove_bomb(self):
        self.bomb_number -= 1

    def get_bomb_number(self):
        return self.bomb_number

    def hit(self):
        self.player_hearts -= 1

    def set_player_hearts(self, number):
        self.player_hearts = number

    def get_heats_number(self):
        return self.player_hearts

    def player_position_reset(self):
        self.player_rect.x = self.x_start
        self.player_rect.y = self.y_start

import pygame, random


class Enemy:

    def __init__(self, spawn_rect, bug, death):

        r = random.choice(spawn_rect)

        self.immune_to_dmg = True
        self.spawn_tick = pygame.time.get_ticks()
        self.to_remove = False

        self.spawn_rect = spawn_rect
        self.turn_rect = []
        self.enemy_rect = pygame.Rect(r.x, r.y, 32, 32)
        self.movement = [0, 0]
        self.enemy_hp = 100
        self.unstuck_tick = 0

        self.directions = {'right', 'left', 'up', 'down'}
        self.direction = 'right'

        self.flip = False
        self.angle = 90
        self.start = True
        self.coords = []
        self.enemy_stuck = False
        self.enemy_hardstuck = False

        self.frame = 0
        self.death_frame = 0

        self.death_animation = death
        self.bug_animation = bug

        self.find_place_to_turn()

    def draw_enemy(self, scroll, display):

        if self.enemy_hp > 0:
            if self.enemy_stuck is False:
                temp = pygame.transform.rotate(self.bug_animation[self.frame], self.angle)
                display.blit(pygame.transform.flip(temp, self.flip, False),
                                                  (self.enemy_rect.x - scroll[0], self.enemy_rect.y - scroll[1]))
                self.frame += 1
                if self.frame % len(self.bug_animation) == 0:
                    self.frame = 0
            else:
                display.blit(self.bug_animation[0], (self.enemy_rect.x - scroll[0], self.enemy_rect.y - scroll[1]))
        else:
            display.blit(self.death_animation[self.death_frame], (self.enemy_rect.x - scroll[0], self.enemy_rect.y - scroll[1]))
            self.death_frame += 1
            if self.death_frame % len(self.death_animation) == 0:
                self.to_remove = True
                self.death_frame = 0

    def move_enemy(self, map_rect, bomb_rect):
        self.coords.append([self.enemy_rect.x, self.enemy_rect.y])

        if len(self.coords) == 2:
            if self.coords[0] == self.coords[1]:
                self.enemy_stuck = True
                if pygame.time.get_ticks() - self.unstuck_tick > 10000:
                    self.enemy_hardstuck = True
            else:
                self.unstuck_tick = pygame.time.get_ticks()
                self.enemy_hardstuck = False
                self.enemy_stuck = False

        if pygame.time.get_ticks() - self.spawn_tick >= 1000:
            self.immune_to_dmg = False
        if self.start is True:
            self.direction = random.choice(list(self.directions))
            self.start = False

        if self.enemy_hardstuck is True:
            self.direction = 'idle'
            if pygame.time.get_ticks() % 5000 >= 4000:
                self.direction = random.choice(list(self.directions))
                self.enemy_hardstuck = False

        if self.direction == 'right':
            self.movement[0] = 1
            self.angle = 270
        elif self.direction == 'left':
            self.movement[0] = -1
            self.angle = 270
        elif self.direction == 'up':
            self.movement[1] = -1
            self.angle = 360
        elif self.direction == 'down':
            self.movement[1] = 1
            self.angle = 180
        elif self.direction == 'idle':
            self.movement = [0, 0]
            self.angle = 180
        if self.direction == 'left':
            self.flip = True
        else:
            self.flip = False

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

        self.movement = [0, 0]

        if self.enemy_stuck is True:
            self.flip = False

        if len(self.coords) == 2:
            self.coords.pop(-1)

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

    def take_damage(self, damage):
        if self.immune_to_dmg is False:
            self.enemy_hp -= damage

            if self.enemy_hp > 0:
                if self.direction == 'right':
                    self.enemy_rect.x -= 5
                elif self.direction == 'left':
                    self.enemy_rect.x += 5
                elif self.direction == 'up':
                    self.enemy_rect.y -= 5
                elif self.direction == 'down':
                    self.enemy_rect.y += 5

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

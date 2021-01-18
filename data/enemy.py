import pygame, random


class Enemy(pygame.sprite.Sprite):

    def __init__(self, spawn_rect, bug, death, type='normal'):
        pygame.sprite.Sprite.__init__(self)
        r = random.choice(spawn_rect)
        self.rect = bug[0].get_rect()
        self.type = type

        if type == 'mutant':
            self.speed = .3
        else:
            self.speed = .2

        self.friction = -.08
        self.max_velocity = 6
        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(r.x, r.y)

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.immune_to_dmg = False
        self.damage_tick = 0

        self.spawn_tick = pygame.time.get_ticks()
        self.to_remove = False
        self.stuck = False
        self.on_bomb = False

        self.turn_rect = []

        if type == 'mutant':
            self.color = (255, 0, 144)
            self.enemy_hp = 300
        else:
            self.enemy_hp = 100

        self.directions = ['right', 'left', 'up', 'down']
        self.direction = random.choice(self.directions)

        self.flip = False
        self.angle = 90

        self.frame = 0
        self.death_frame = 0
        self.anim_tick = 0

        self.death_animation = death
        self.bug_animation = bug

    def draw_enemy(self, scroll, display):

        if self.enemy_hp > 0:
            tick = pygame.time.get_ticks()
            if self.stuck is False:
                img = pygame.transform.rotate(self.bug_animation[self.frame], self.angle)
            else:
                self.flip = False
                self.angle = 0
                img = pygame.transform.rotate(self.bug_animation[0], self.angle)
            if self.type == 'mutant':
                temp = pygame.Surface(img.get_size())
                temp.fill(self.color)

                output_image = img.copy()
                output_image.blit(temp, (0, 0), special_flags=pygame.BLEND_MULT)
            else:
                output_image = img

            display.blit(pygame.transform.flip(output_image, self.flip, False), (self.rect.x - scroll[0], self.rect.y - scroll[1]))

            if tick - 100 > self.anim_tick:
                self.anim_tick = tick
                self.frame += 1
                if self.frame % len(self.bug_animation) == 0:
                    self.frame = 0

        else:
            tick = pygame.time.get_ticks()
            display.blit(self.death_animation[self.death_frame], (self.rect.x - scroll[0], self.rect.y - scroll[1]))
            if tick - 100 > self.anim_tick:
                self.death_frame += 1
                if self.death_frame % len(self.death_animation) == 0:
                    self.to_remove = True
                    self.death_frame = 0

    def update(self, map_rect, bomb_rect, turn_rect, player_pos, dt):

        if self.immune_to_dmg is True:
            if pygame.time.get_ticks() - 500 > self.damage_tick:
                self.immune_to_dmg = False

        self.acceleration.x = 0
        self.acceleration.y = 0

        if self.direction == 'right':
            self.acceleration.x += self.speed
            self.angle = 270
        elif self.direction == 'left':
            self.acceleration.x -= self.speed
            self.angle = 270
        elif self.direction == 'up':
            self.acceleration.y -= self.speed
            self.angle = 0
        elif self.direction == 'down':
            self.acceleration.y += self.speed
            self.angle = 180
        elif self.direction == 'idle':
            self.acceleration.x = 0
            self.acceleration.y = 0
            self.angle = 180
        if self.direction == 'left':
            self.flip = True
        else:
            self.flip = False

        if self.type == 'mutant':
            self.speed = .3
            if abs(player_pos[0] - self.rect.center[0]) < 32:
                if player_pos[1] > self.rect.center[1] and self.direction == 'down':
                    self.acceleration *= 2
                if player_pos[1] < self.rect.center[1] and self.direction == 'up':
                    self.acceleration *= 2
            if abs(player_pos[1] - self.rect.center[1]) < 32:
                if player_pos[0] > self.rect.center[0] and self.direction == 'right':
                    self.acceleration *= 2
                if player_pos[0] < self.rect.center[0] and self.direction == 'left':
                    self.acceleration *= 2

        self.acceleration += self.velocity * self.friction

        if abs(self.velocity.x) < self.max_velocity:
            self.velocity.x += self.acceleration.x * dt
        if abs(self.velocity.y) < self.max_velocity:
            self.velocity.y += self.acceleration.y * dt

        self.position += self.velocity * dt + (self.acceleration * .5) * (dt * dt)
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        collisions = self.collision_check(map_rect)
        if self.on_bomb is False:
            collisions += self.collision_check(bomb_rect)

        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.x - self.rect.width
                self.rect.x = self.position.x
                self.direction = random.choice(self.directions)
                self.velocity.x = 0
                self.velocity.y = 0
            elif self.velocity.x < 0:
                self.position.x = tile.x + tile.width
                self.rect.x = self.position.x
                self.direction = random.choice(self.directions)
                self.velocity.x = 0
                self.velocity.y = 0
            if self.velocity.y > 0:
                self.position.y = tile.y - self.rect.height
                self.rect.y = self.position.y
                self.direction = random.choice(self.directions)
                self.velocity.x = 0
                self.velocity.y = 0
            elif self.velocity.y < 0:
                self.position.y = tile.y + self.rect.height
                self.rect.y = self.position.y
                self.direction = random.choice(self.directions)
                self.velocity.x = 0
                self.velocity.y = 0

        rand = random.randint(0, 100)
        for tile in turn_rect:
            if tile[0] == self.rect.x and tile[1] == self.rect.y:
                if rand % 3 == 0:
                    self.direction = random.choice(list(self.directions))
                    self.velocity.x = 0
                    self.velocity.y = 0
                break

        if self.type == 'normal':
            if abs(self.velocity.x) < .5 and abs(self.velocity.y) < .5:
                self.stuck = True
            else:
                self.stuck = False
        elif self.type == 'mutant':
            if abs(self.velocity.x) < 1 and abs(self.velocity.y) < 1:
                self.stuck = True
            else:
                self.stuck = False

    def take_damage(self, damage):
        if self.immune_to_dmg is False:
            self.enemy_hp -= damage
            self.immune_to_dmg = True
            self.damage_tick = pygame.time.get_ticks()

    def collision_check(self, tiles):
        hit_rect = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_rect.append(tile)
        return hit_rect

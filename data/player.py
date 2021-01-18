import pygame
from data.images import Spritesheet
from data.cutscene import CutScene0


class Player(pygame.sprite.Sprite):

    def __init__(self, window):
        pygame.sprite.Sprite.__init__(self)

        x_start = 232
        y_start = 256
        self.rect = pygame.Rect(x_start, y_start, 16, 16)
        self.left_key, self.right_key, self.up_key, self.down_key = False, False, False, False
        self.text_color = (255, 219, 88)

        # new

        self.speed = 1
        self.friction = -.45
        self.position = pygame.math.Vector2(x_start, y_start)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)

        self.busy = False
        self.in_cutscene = False

        self.talk_pos = []
        self.talk = False
        self.quotes = ['THERE IS TOO DARK']
        self.shoot_delay = 0

        # stats

        self.level = 1
        self.current_health = 100
        self.max_health = 100
        self.coins = 0
        self.immune_to_dmg = False
        self.dmg_tick = 0

        # health bar

        window_w = window[0] / 2
        window_h = window[1] / 2

        self.font_size = int(window_h * .05)

        self.health_bar = pygame.Rect(0, 0, window_w * .25, window_h * .05)
        self.health_bar.topright = (window_w * .95, window_h * .03)
        self.bar_width = self.health_bar.width
        self.border = pygame.Rect(0, 0, window_w * .25, window_h * .05)
        self.border.topright = (window_w * .95, window_h * .03)
        self.text_pos = self.health_bar.center

        # other bar
        self.current_xp = 0
        self.next_lvl = 1000

        self.xp_bar = pygame.Rect(0, 0, window_w * .25, window_h * .05)
        self.xp_bar.topleft = (window_w * .05, window_h * .03)
        self.xp_width = self.xp_bar.width

        self.xp_border = pygame.Rect(0, 0, window_w * .25, window_h * .05)
        self.xp_border.topleft = (window_w * .05, window_h * .03)
        self.xp_text_pos = self.xp_bar.center

        self.gain_xp(100)

        # old 10

        self.frame = 0

        self.action = 'idle'
        self.direction = self.action
        self.last_tick = 0
        self.player_stuck = False

        self.on_bomb = False
        self.animation_left = []
        self.animation_right = []
        self.animation_up = []
        self.animation_down = []
        self.load_images()
        self.img = self.animation_down[0]
        self.img_color = (255, 0, 255)

    def load_images(self):
        spritesheet = Spritesheet('data/assets/sprites/spritesheet.png')
        for n in range(8):
            path_r = 'player_side_' + str(n)
            path_d = 'player_down_' + str(n)
            path_u = 'player_up_' + str(n)

            image_r = spritesheet.parse_sprite(path_r)
            image_d = spritesheet.parse_sprite(path_d)
            image_u = spritesheet.parse_sprite(path_u)
            self.animation_right.append(image_r)
            self.animation_down.append(image_d)
            self.animation_up.append(image_u)
            self.animation_left.append(pygame.transform.flip(image_r, True, False))

    def draw(self, s, display, font):
        temp = pygame.Surface(self.img.get_size())
        temp.fill(self.img_color)

        output_image = self.img.copy()
        output_image.blit(temp, (0, 0), special_flags=pygame.BLEND_MULT)

        self.draw_bars(display, font)
        display.blit(output_image, (self.rect.x - 8 - s. x, self.rect.y - 16 - s.y))

    def draw_bars(self, display, font):

        pygame.draw.rect(display, (200, 0, 0), self.health_bar, border_radius=5)
        pygame.draw.rect(display, (69, 69, 69), self.border, 2, border_radius=5)

        pygame.draw.rect(display, (0, 200, 0), self.xp_bar, border_radius=5)
        pygame.draw.rect(display, (69, 69, 69), self.xp_border, 2, border_radius=5)

        self.draw_text(display, font,  str(self.current_health) + ' / ' + str(self.max_health), self.text_pos)
        self.draw_text(display, font, str(self.current_xp) + ' / ' + str(self.next_lvl), self.xp_text_pos)

    def draw_text(self, display, font, t, pos):
        font = pygame.font.Font(font, self.font_size)
        text = t
        text_surface = font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        display.blit(text_surface, text_rect)

    def gain_xp(self, xp):
        self.current_xp += xp
        percent = self.current_xp / self.next_lvl
        self.xp_bar.width = self.xp_width * percent

    def take_damage(self, damage):

        if self.immune_to_dmg is False:
            self.current_health -= damage
            percent = self.current_health / self.max_health
            self.health_bar.width = self.bar_width * percent
            self.immune_to_dmg = True
            self.dmg_tick = pygame.time.get_ticks()

    def heal(self, health):
        for i in range(health):
            if self.current_health != self.max_health:
                self.current_health += 1
                percent = self.current_health / self.max_health
                self.health_bar.width = self.bar_width * percent
            else:
                break

    def update(self, map_rect, dt, cut_scene_menager):

        current_tick = pygame.time.get_ticks()

        if self.immune_to_dmg is True:
            if current_tick - 500 > self.dmg_tick:
                self.immune_to_dmg = False

        if self.last_tick == 0:
            cut_scene_menager.start_cut_scene(CutScene0(self))
            self.last_tick += 1

        self.player_stuck = False

        self.acceleration.x = 0
        self.acceleration.y = 0

        if self.busy is False and self.in_cutscene is False:
            if self.left_key:
                self.acceleration.x -= self.speed
                self.action = 'left'
            if self.right_key:
                self.acceleration.x += self.speed
                self.action = 'right'
            if self.down_key:
                self.acceleration.y += self.speed
                self.action = 'down'
            if self.up_key:
                self.acceleration.y -= self.speed
                self.action = 'up'
        else:
            self.shoot_delay = pygame.time.get_ticks()

        if self.acceleration.x == 0 and self.acceleration.y == 0:
            self.action = 'idle'
        else:
            self.direction = self.action

        self.acceleration.x += self.velocity.x * self.friction
        if abs(self.velocity.x) < 5:
            self.velocity.x += self.acceleration.x * dt

        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.rect.x = self.position.x

        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.velocity.x > 0:
                self.position.x = tile.left - self.rect.w
                self.rect.x = self.position.x
                if self.action == 'right':
                    self.player_stuck = True
            elif self.velocity.x < 0:
                self.position.x = tile.right
                self.rect.x = self.position.x
                if self.action == 'left':
                    self.player_stuck = True

        self.acceleration.y += self.velocity.y * self.friction
        if abs(self.velocity.y) < 5:
            self.velocity.y += self.acceleration.y * dt

        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        self.rect.y = self.position.y

        hit_list = self.collision_test(map_rect)

        for tile in hit_list:
            if self.velocity.y > 0:
                self.position.y = tile.top - self.rect.h
                self.rect.y = self.position.y
                if self.action == 'down':
                    self.player_stuck = True
            elif self.velocity.y < 0:
                self.position.y = tile.bottom
                self.rect.y = self.position.y
                if self.action == 'up':
                    self.player_stuck = True

        self.animate()

    def animate(self):
        tick = pygame.time.get_ticks()
        if self.action == 'idle' or self.player_stuck is True:
            if self.direction == 'left':
                self.img = self.animation_left[0]
            elif self.direction == 'right':
                self.img = self.animation_right[0]
            elif self.direction == 'down':
                self.img = self.animation_down[0]
            elif self.direction == 'up':
                self.img = self.animation_up[0]

        else:
            if tick - self.last_tick > 75:
                self.last_tick = tick
                self.frame = (self.frame + 1) % len(self.animation_down)

            if self.action == 'left':
                self.img = self.animation_left[self.frame]
            elif self.action == 'right':
                self.img = self.animation_right[self.frame]
            elif self.action == 'down':
                self.img = self.animation_down[self.frame]
            elif self.action == 'up':
                self.img = self.animation_up[self.frame]

    def collision_test(self, map_rect):
        hit_list = []
        for tile in map_rect:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

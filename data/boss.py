import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self,  x, y, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.friction = -.12
        self.img = pygame.image.load('data/assets/sprites/boss.png')
        self.rect = self.img.get_rect()

        self.friction = -.25
        self.position = pygame.math.Vector2(x / 2 - 32, y / 2)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.go_to_vector = pygame.math.Vector2(0, 0)

        self.shoot = False
        self.last_tick = 0
        self.mutated = False
        self.immune_to_dmg = False
        self.spin = False
        self.angle = 0
        self.value = 0

        self.window_w = width / 2
        self.window_h = height / 2
        self.red = (255, 0, 0)
        self.black = (0, 0, 0)
        self.max_health = width / 2
        self.health = width / 2
        self.ramka = pygame.Rect(20, self.window_h - 40, self.health - 40, 20)

    def draw_boss(self, scroll, display):

        if self.spin is True:
            display.blit(pygame.transform.rotate(self.img, self.angle), (self.rect.x - scroll.x, self.rect.y - scroll.y))
            self.angle += 10
            if self.angle == 1800:
                self.angle = 0
                self.spin = False
                self.mutated = True
        else:
            display.blit(self.img, (self.rect.x - scroll.x, self.rect.y - scroll.y))

    def update(self, map_rect, player_rect, dt):

        self.acceleration.x = 0
        self.acceleration.y = 0

        if self.max_health < self.health * 2:
            self.value = 25
            tick = pygame.time.get_ticks()
            if tick - self.last_tick > 2000:
                self.last_tick = tick

                if self.position.x > player_rect[0]:
                    self.go_to_vector.x = player_rect[0] - 100
                else:
                    self.go_to_vector.x = player_rect[0] + 100

                if self.position.y > player_rect[1]:
                    self.go_to_vector.y = player_rect[1] - 100
                else:
                    self.go_to_vector.y = player_rect[1] + 100

        elif self.max_health > self.health * 2 and self.mutated is False:
            if 2 / 5 * self.window_w <= self.position.x <= 3 / 5 * self.window_w:
                self.spin = True
                self.go_to_vector.x = self.window_w * 3
                self.value = 200
                # self.mutated = True
            else:
                self.immune_to_dmg = True
                if self.spin is False:
                    self.go_to_vector.x = self.window_w / 2
                    self.go_to_vector.y = self.window_h / 2

        elif self.max_health > self.health * 2 and self.mutated is True:
            print(self.rect)
            if self.position.x >= 2 * self.window_w:
                self.go_to_vector.y = player_rect[1]
                self.go_to_vector.x = -self.window_w * 2
            elif self.position.x <= -self.window_w:
                self.go_to_vector.y = player_rect[1]
                self.go_to_vector.x = 3 * self.window_w

        self.acceleration.x += (self.go_to_vector.x - self.position.x) / self.value
        self.acceleration.y += (self.go_to_vector.y - self.position.y) / self.value
        # self.acceleration *= 2

        self.acceleration.x += self.velocity.x * self.friction
        self.acceleration.y += self.velocity.y * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(2)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * .5) * (dt * dt)
        self.position.y += self.velocity.y * dt + (self.acceleration.y * .5) * (dt * dt)
        if self.spin is False:
            self.rect.center = self.position

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0
        if abs(self.velocity.y) < .01:
            self.velocity.y = 0

    def draw_health_bar(self, display):
        health_bar = pygame.Rect(20, self.window_h - 40, self.health - 40, 20)
        pygame.draw.rect(display, self.red, health_bar)
        pygame.draw.rect(display, self.black, self.ramka, 2)

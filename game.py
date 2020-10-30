from bomberman.menu import *
from bomberman.player import Player
from bomberman.bomb import Bomb
from bomberman.map import Map
from bomberman.enemy import Enemy


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # loops
        self.running = True
        self.playing = False

        # inputs
        self.click = False
        self.back_key = False
        self.space_key = False

        # screen
        self.window_width = 1680
        self.window_height = 1050
        self.game_window_size = 0

        self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN, 0, 32)
        self.display = pygame.Surface((int(self.window_width / 2), int(self.window_height / 2)))
        self.menu_display = pygame.Surface((int(self.window_width), int(self.window_height)))

        # font, colors
        self.font_name = 'assets/fonts/bank_gothic.ttf'
        self.title_font_name = 'assets/fonts/title_font.ttf'
        self.black = (0, 0, 0)
        self.white = (143,168,203)
        self.mustard = (255, 219, 88)
        self.magenta = (255, 0, 144)

        # menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.current_menu = self.main_menu

        # maps
        self.current_level = 0
        self.number_of_levels = 2
        self.spawn_rect = []
        self.levels = []
        self.map_rect = 0

        for n in range(self.number_of_levels):
            level = Map(n)
            self.levels.append(level)

        for level in self.levels:
            self.spawn_rect.append(level.get_spawn_rect())

        # player
        self.player_0 = Player(self.window_width, self.window_height, self.spawn_rect[self.current_level])
        self.scroll = [0, 0]
        self.game_start = False
        self.score = 0
        self.time = 120
        self.hearts_number = 3
        self.temp_countdown = 1000

        # bombs
        self.bomb_dropped = False
        self.bomb_pause = False
        self.bombs = []
        self.bomb_ticks = []
        self.bomb_rect = []
        self.explosion_length = 1
        self.door_explosion_delay = False
        self.temp_tick = 0

        # enemies
        self.enemies = []

        for n in range(3 * (self.current_level + 1)):
            enemy = Enemy(self.spawn_rect[self.current_level], self.display)
            self.enemies.append(enemy)

        # images
        self.heart_img = pygame.image.load('assets/sprites/heart.png')

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.update_game()
            self.draw_game()
            self.countdown()

            # surface.blit(pygame.transform.scale(display, windowSize), (0, 0))
            self.window.blit(pygame.transform.scale(self.display, (self.window_width, self.window_height)), (0, 0))
            pygame.display.update()
            self.clock.tick(100)
            self.reset_keys()

    def check_events(self):
        if self.playing is True:
            pygame.mouse.set_visible(False)
        if self.playing is False:
            pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.current_menu.run_display = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.bomb_pause is False and self.player_0.get_bomb_number() != 0:
                        self.player_0.remove_bomb()
                        self.bomb_dropped = True
                    self.space_key = True

                if event.key == pygame.K_ESCAPE:
                    self.back_key = True

    def reset_keys(self):
        self.click = False
        self.back_key = False
        self.space_key = False

    def draw_text(self, text, size, x, y, color, type='menu', font_type='regular'):
        if font_type == 'regular':
            font = pygame.font.Font(self.font_name, size)
        if font_type == 'title':
            font = pygame.font.Font(self.title_font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if type == 'game':
            self.display.blit(text_surface, text_rect)
            return text_rect
        else:
            self.menu_display.blit(text_surface, text_rect)
            return text_rect

    def update_game(self):
        # pause
        if self.back_key is True:
            self.current_menu = self.pause_menu
            self.playing = False

        # map
        self.map_rect = self.levels[self.current_level].get_tile_rect()

        # player
        self.player_0.move_player(self.map_rect)
        self.scroll = self.player_0.scroll()

        # bomb
        if self.bomb_dropped is True:
            current_tick = pygame.time.get_ticks()
            self.bomb_ticks.append(current_tick)

            bomb = Bomb(self.player_0.get_player_rect(), self.display, self.levels[self.current_level].get_hard_wall(),
                        self.explosion_length)
            self.bomb_rect.append(bomb.get_bomb_rect())
            bomb.move_bomb(self.levels[self.current_level].get_tile_rect())
            self.bombs.append(bomb)

            self.bomb_pause = True
            self.bomb_dropped = False

        if len(self.bomb_ticks) != 0:
            if self.bomb_pause is True and pygame.time.get_ticks() - self.bomb_ticks[-1] > 500:
                self.bomb_pause = False
        else:
            self.bomb_pause = False

        # removing bombs
        for t in self.bomb_ticks:
            if pygame.time.get_ticks() - t > 3000 and len(self.bombs) != 0:
                explosion_rect = self.bombs[0].get_explosion_rect()
                self.levels[self.current_level].wall_destroying(explosion_rect)

                # player, enemy dmg
                for tile in explosion_rect:
                    if tile.colliderect(self.player_0.get_player_rect()):
                        self.player_0.hit()
                        self.game_over()

                    for enemy in self.enemies:
                        if tile.colliderect(enemy.get_rect()):
                            self.score += 10
                            enemy.take_damage(200)

                if pygame.time.get_ticks() - t > 4000:
                    self.bombs.pop(0)
                    self.player_0.add_bomb()
                    self.bomb_rect.pop(0)
                    self.bomb_ticks.pop(0)

        # enemies
        for enemy in self.enemies:
            enemy.move_enemy(self.map_rect, self.bomb_rect)
            enemy_rect = enemy.get_rect()
            if enemy_rect.colliderect(self.player_0.get_player_rect()):
                self.player_0.hit()
                self.game_over()
            if enemy.get_hp() <= 0:
                self.enemies.remove(enemy)

        # door
        if self.door_explosion_delay is False:
            if self.levels[self.current_level].are_door_spawned() is True:
                door_rect = self.levels[self.current_level].get_door_rect()
                for bomb in self.bombs:
                    explosion_rect = bomb.get_explosion_rect()
                    for rect in explosion_rect:
                        if rect.colliderect(door_rect):
                            if bomb.bomb_exploded is True:
                                for m in range((self.current_level + 1) * 3):
                                    enemy = Enemy(self.spawn_rect[self.current_level], self.display, door_rect.x,
                                                  door_rect.y, True)
                                    self.enemies.append(enemy)
                                self.temp_tick = pygame.time.get_ticks()
                                self.door_explosion_delay = True

        if self.door_explosion_delay is True:
            if pygame.time.get_ticks() - self.temp_tick >= 2000:
                self.door_explosion_delay = False

        if len(self.enemies) == 0 and self.levels[self.current_level].check_door() is False:
            self.levels[self.current_level].open_the_door()
            print("all dead")

        if self.levels[self.current_level].check_door() is True and self.levels[self.current_level].are_door_spawned():
            if self.levels[self.current_level].get_door_rect().colliderect(self.player_0.get_player_rect()):
                self.current_level += 1
                if self.current_level == 2:
                    self.current_level = 0
                self.game_over()

        # coins
        bomb_coins_rect = self.levels[self.current_level].get_bomb_coin_rect()
        explosion_coins_rect = self.levels[self.current_level].get_explosion_coin_rect()

        for rect in bomb_coins_rect:
            if self.player_0.get_player_rect().colliderect(rect):
                self.player_0.add_bomb()
                self.levels[self.current_level].coin_picking(rect, 'bomb')

        for rect in explosion_coins_rect:
            if self.player_0.get_player_rect().colliderect(rect):
                self.explosion_length += 1
                self.levels[self.current_level].coin_picking(rect, 'explosion')

    def draw_game(self):
        self.display.fill(self.mustard)

        self.levels[self.current_level].tile_map_reset()
        self.levels[self.current_level].display_map(self.scroll, self.display)

        for bomb in self.bombs:
            bomb.draw_bomb(self.scroll)
            bomb.explosion()
            bomb.draw_explosion(self.scroll)

        for enemy in self.enemies:
            enemy.draw_enemy(self.scroll)

        self.player_0.draw_player(self.scroll, self.display)

        # HUD
        bombs_number = self.player_0.get_bomb_number()
        self.draw_text('SCORE: ' + str(self.score), 10, 75, 25, self.white, 'game')
        self.draw_text('TIME: ' + str(self.time), 10, self.window_width / 4, 25, self.white, 'game')
        temp_rect = self.draw_text('LIVES: ', 10, self.window_width / 2 - 125, 25, self.white, 'game')
        x, y = temp_rect.topright
        for n in range(self.player_0.get_heats_number()):
            temp_rect = pygame.Rect(x + (n * 32), y - 10, 32, 32)
            self.display.blit(self.heart_img, (temp_rect.x, temp_rect.y))
        self.draw_text('BOMBS: ' + str(bombs_number), 10, 75, self.window_height / 2 - 25, self.white, 'game')
        self.draw_text('EXPLOSION: ' + str(self.explosion_length), 10, 75, self.window_height / 2 - 35, self.white,
                       'game')

    def countdown(self):
        tick = pygame.time.get_ticks()
        if tick - self.temp_countdown >= 1000:
            self.temp_countdown = pygame.time.get_ticks()
            self.time -= 1
        if self.time < 0:
            self.hearts_number -= 1
            self.game_over()

    def game_over(self):
        self.time = 120
        self.bomb_pause = True
        self.player_0.player_position_reset()
        self.bombs = []
        self.bomb_ticks = []
        self.enemies = []
        self.levels[self.current_level].door_remove()
        self.levels[self.current_level].generate_map()

        self.spawn_rect[self.current_level] = self.levels[self.current_level].get_spawn_rect()

        for n in range(3 * (self.current_level + 1)):
            enemy = Enemy(self.spawn_rect[self.current_level], self.display)
            self.enemies.append(enemy)

        if self.player_0.get_heats_number() > 0:
            pass
        else:
            pass

        self.playing = False
        self.current_menu = self.game_over_menu

    def get_running(self):
        return self.running

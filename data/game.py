from data.menu import *
from data.player import Player
from data.bomb import Bomb
from data.enemy import Enemy
from data.images import Spritesheet
# from data.npc import Npc
from data.missile import Missile
from data.tiles import *
from data.camera import *
from data.boss import Boss


class Game:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # loops
        self.running = True
        self.playing = False
        self.game_reset = False

        # inputs
        self.click = False
        self.back_key = False
        self.drop_bomb = False
        self.shoot = False
        self.kill_all_enemies = False
        self.enter_the_door = False
        self.talk = False

        # screen
        self.window_width = 1280
        self.window_height = 720
        self.window = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)
        self.display = pygame.Surface((int(self.window_width / 2), int(self.window_height / 2)))
        self.menu_display = pygame.Surface((int(self.window_width), int(self.window_height)))
        self.FPS = 60

        # music
        # pygame.mixer.music.load('assets/sounds/8bit.mp3')

        # font, colors
        self.font_name = 'data/assets/fonts/bank_gothic.ttf'
        self.title_font_name = 'data/assets/fonts/title_font.ttf'
        self.background = (34, 30, 49)
        self.black = self.background
        self.white = (143, 168, 203)
        self.mustard = (255, 219, 88)
        self.magenta = (255, 0, 144)

        # images !!!
        self.heart_img = pygame.image.load('data/assets/sprites/heart.png')

        map_sheet = Spritesheet('data/assets/sprites/walls/tileset.png')
        self.spritesheet = Spritesheet('data/assets/sprites/spritesheet.png')
        bug_animation_sheet = Spritesheet('data/assets/sprites/enemy/bug.png')
        death_animation_sheet = Spritesheet('data/assets/sprites/destruction/destruction.png')

        self.death_animation = []
        self.bug_animation = []
        self.bomb_animation = []

        duration, number_of_images = death_animation_sheet.get_info()

        for n in range(number_of_images):
            for m in range(duration):
                name = "explosion_" + str(n)
                self.death_animation.append(death_animation_sheet.parse_sprite(name))

        duration, number_of_images = bug_animation_sheet.get_info()

        for n in range(number_of_images):
            for m in range(duration):
                name = "bug_" + str(n)
                self.bug_animation.append(bug_animation_sheet.parse_sprite(name))

        number_of_images, duration = 5, 7

        for n in range(number_of_images):
            for m in range(duration):
                name = "bomb_" + str(n)
                self.bomb_animation.append(self.spritesheet.parse_sprite(name))

        # maps
        self.number_of_levels = 5

        self.current_level = 0
        self.levels = []

        for i in range(self.number_of_levels):
            path = 'data/assets/maps/level_' + str(i) + '.csv'
            level = TileMap(path, map_sheet, i)
            self.levels.append(level)

        # menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.message_screen = GenerateMessage(self)
        self.current_menu = self.main_menu

        # player
        self.player_0 = Player()

        self.score = 0
        self.time = 120
        self.temp_countdown = 1000
        self.dead_tick = 0

        # camera
        self.camera = Camera(self.player_0)
        self.follow = Follow(self.camera, self.player_0)
        self.border = Border(self.camera, self.player_0)
        self.auto = Auto(self.camera, self.player_0)
        self.camera.set_method(self.follow)

        # NPCs
        # self.npc_0 = Npc(self.levels[0].get_spawn_rect(), self)
        self.talk_to_npc = False

        # bombs
        self.bomb_dropped = False
        self.bomb_pause = True
        self.bombs = []
        self.bomb_ticks = []
        self.bomb_rect = []
        self.explosion_length = 1

        # missiles
        self.missiles = []
        self.direction = 'idle'

        # enemies
        self.enemies = []
        self.boss = None

        # temp
        self.temp_variable = True

    def game_loop(self):
        while self.playing:
            self.check_events()

            self.update_game()
            self.draw_game()

            # surface.blit(pygame.transform.scale(display, windowSize), (0, 0))
            self.window.blit(pygame.transform.scale(self.display, (self.window_width, self.window_height)), (0, 0))
            pygame.display.update()
            self.clock.tick(self.FPS)
            self.reset_keys()

    def update_game(self):
        # pause
        if self.back_key is True:
            self.current_menu = self.pause_menu
            self.playing = False

        # map
        map_rect = self.levels[self.current_level].get_colliders()
        # self.map_rect.append(self.npc_0.npc_rect)

        if len(self.enemies) == 0 and self.levels[self.current_level].map_completed is False:
            self.levels[self.current_level].map_completed = True
            self.levels[self.current_level].load_doors()

        # player
        self.player_0.move_player(map_rect, 1)
        self.camera.scroll()

        # missiles

        if self.shoot is True:
            missile = Missile(self.player_0.rect.x, self.player_0.rect.y, self.player_0.action, True, 'bullet')
            self.missiles.append(missile)

        if len(self.missiles) != 0:
            for missile in self.missiles:
                for tile in map_rect:
                    if missile.missile_rect.colliderect(tile):
                        self.missiles.remove(missile)
                        break

                for enemy in self.enemies:
                    if missile.missile_rect.colliderect(enemy.enemy_rect):
                        enemy.take_damage(2)
                        self.missiles.remove(missile)
                        break

                missile.move_missile()

        # bomb
        if self.bomb_dropped is True:
            current_tick = pygame.time.get_ticks()
            self.bomb_ticks.append(current_tick)

            bomb = Bomb(self.player_0.rect, self.levels[self.current_level].get_hard_wall(),
                        self.levels[self.current_level].get_soft_wall(), self.explosion_length)
            self.bomb_rect.append(bomb.bomb_rect)
            bomb.move_bomb(map_rect)
            self.bombs.append(bomb)

            self.bomb_pause = True
            self.bomb_dropped = False

        if len(self.bomb_ticks) != 0:
            if self.bomb_pause is True and pygame.time.get_ticks() - self.bomb_ticks[-1] > 500:
                self.bomb_pause = False
        else:
            self.bomb_pause = False

        x = 0
        temp = 0
        for missile in self.missiles:
            for bomb in self.bombs:
                if missile.missile_rect.colliderect(bomb.bomb_rect):
                    temp = pygame.time.get_ticks() - self.bomb_ticks[x]
                    temp = 3000 - temp
                    self.bomb_ticks[x] -= temp
                    self.missiles.remove(missile)
                x += 1
            x = 0

        # removing bombs
        for t in self.bomb_ticks:
            if pygame.time.get_ticks() - t >= 3000:
                if self.temp_variable is True:
                    self.bombs[0].explosion()
                    self.bombs[0].find_edges()
                    self.temp_variable = False
                explosion_rect = self.bombs[0].explosion_rect
                self.levels[self.current_level].wall_destroying(explosion_rect)

                # player, enemy dmg
                for tile in explosion_rect:
                    for enemy in self.enemies:
                        if tile.colliderect(enemy.enemy_rect) and enemy.immune_to_dmg is False:
                            self.score += 100
                            enemy.take_damage(200)

                for tile in explosion_rect:
                    if tile.colliderect(self.player_0.rect):
                        self.player_0.player_hearts -= 1
                if t is False:
                    t = temp
                if pygame.time.get_ticks() - t >= 3800:
                    self.temp_variable = True
                    self.bombs.pop(0)
                    self.player_0.bomb_number += 1
                    self.bomb_rect.pop(0)
                    self.bomb_ticks.pop(0)

        # enemies

        for enemy in self.enemies:
            if enemy.enemy_hp > 0:
                enemy.move_enemy(map_rect, self.bomb_rect)
            enemy_rect = enemy.enemy_rect
            if enemy_rect.colliderect(self.player_0.rect):
                self.player_0.player_hearts -= 1
                print("enemy hit")
                # self.game_over()
            if enemy.to_remove is True:
                self.enemies.remove(enemy)

        # door
        doors = self.levels[self.current_level].get_door_rect()

        for rect in doors:
            if rect[2] is True:
                temp = pygame.Rect(rect[0].x, rect[0].y + 32, 32, 32)
            else:
                temp = pygame.Rect(rect[0].x, rect[0].y, 32, 32)

            if self.player_0.rect.colliderect(temp):

                if self.enter_the_door is True:
                    if rect[1][2] != 'i' and self.levels[self.current_level].map_completed is True:
                        print("outside")
                        temp = rect[1][1]
                        temp = int(temp)
                        if temp == self.current_level:
                            temp += 1
                        self.current_level = temp
                        self.enter_the_door_function(int(rect[1][1]))

                    else:
                        temp = rect[1][1]
                        print("inside")
                        for door in doors:
                            if door[1][1] == temp and door[0] != rect[0]:
                                print(rect[0], " ", door[0])
                                self.player_0.position.x = door[0].x
                                self.player_0.position.y = door[0].y + 32
                                break
                        break

        # coins
        coins = self.levels[self.current_level].coin
        for coin in coins:
            if self.player_0.rect.colliderect(coin.rect):
                self.player_0.coins += 1
                self.levels[self.current_level].picking(coin.rect, 'coin')

        # cheats
        if self.kill_all_enemies is True:
            self.enemies.clear()

        # npc-player
        """
        in_range = False
        for tile in self.npc_0.talk_rect:
            if self.player_0.get_player_rect().colliderect(tile):
                self.talk_to_npc = True
                in_range = True
        
        if in_range is False:
            self.talk = False

        pygame.mouse.set_visible(self.talk)
        """

        # boss
        directions = ['left', 'right', 'up', 'down']

        if self.boss is not None:
            self.boss.update(self.levels[self.current_level].wall, self.player_0.rect.center, 1)
            if self.boss.shoot is True:
                for i in directions:
                    pass
                    # missile = Missile(self.boss.x, self.boss.y, i, False, 'bullet')
                    # self.missiles.append(missile)

            for missile in self.missiles:
                if self.boss.rect.colliderect(missile.missile_rect):
                    self.boss.health -= 1
                    self.missiles.remove(missile)

            x = 0
            for bomb in self.bombs:
                if self.boss.rect.colliderect(bomb.bomb_rect):
                    temp = pygame.time.get_ticks() - self.bomb_ticks[x]
                    temp = 3000 - temp
                    self.bomb_ticks[x] -= temp
                    if self.boss.immune_to_dmg is False:
                        self.boss.health -= 10
                x += 1

        # other
        if self.player_0.player_hearts > 0:
            self.dead_tick = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.dead_tick >= 2000 and self.player_0.player_hearts <= 0:
            pass
            # self.game_over()

    def draw_game(self):

        self.display.fill(self.background)

        self.levels[self.current_level].draw_map(self.camera.offset, self.display)

        for bomb in self.bombs:
            bomb.draw_bomb(self.camera.offset, self.display, self.bomb_animation)
            bomb.draw_explosion(self.camera.offset, self.display)

        for enemy in self.enemies:
            enemy.draw_enemy(self.camera.offset, self.display)

        for missile in self.missiles:
            missile.draw_missile(self.camera.offset, self.display)

        self.player_0.draw_player(self.camera.offset, self.display)

        # boss

        if self.boss is not None:
            self.boss.draw_boss(self.camera.offset, self.display)
            self.boss.draw_health_bar(self.display)

        """
        if self.current_level == 0:
            self.npc_0.draw_npc(self.scroll, self.display)
            if self.talk is True:
                self.npc_0.draw_chat(self.display)
        """
        # HUD
        self.draw_text('SCORE: ' + str(self.score), 10, 75, 25, self.mustard, 'game')
        self.draw_text('TIME: ' + str(self.time), 10, self.window_width / 4, 25, self.mustard, 'game')
        temp_rect = self.draw_text('LIVES: ', 10, self.window_width / 2 - 125, 25, self.mustard, 'game')
        x, y = temp_rect.topright
        for n in range(self.player_0.bomb_number):
            temp_rect = pygame.Rect(x + (n * 32), y - 10, 32, 32)
            self.display.blit(self.heart_img, (temp_rect.x, temp_rect.y))

    def enter_the_door_function(self, spawn):

        # boss
        if self.current_level == 4:
            x, y = self.levels[self.current_level].get_level_size()
            self.boss = Boss(x, y, self.window_width, self.window_height)

        for rect in self.levels[self.current_level].get_door_rect():
            if int(rect[1][1]) == spawn:
                self.player_0.position.x = rect[0].x
                self.player_0.position.y = rect[0].y
                if rect[2] is True:
                    self.player_0.position.y += 32
                else:
                    self.player_0.position.y += 16

        self.time = 120
        self.bomb_pause = True
        self.temp_variable = True

        for n in range(len(self.bombs)):
            self.player_0.bomb_number += 1

        self.bombs = []
        self.bomb_ticks = []
        self.enemies = []

        if self.player_0.bomb_number == 0:
            self.player_0.bomb_number = 1

        if self.levels[self.current_level].map_completed is False and self.levels[self.current_level].without_enemies is False:
            for n in range(3 * (self.current_level + 1)):
                enemy = Enemy(self.levels[self.current_level].get_spawn_rect(), self.bug_animation, self.death_animation)
                self.enemies.append(enemy)

        self.playing = False
        self.current_menu = self.message_screen
    
    def game_over(self):

        self.time = 120
        self.bomb_pause = True
        self.temp_variable = True
        self.current_level = 0

        self.player_0.bomb_number = 1
        self.explosion_length = 1
        self.current_level = 0
        self.score = 0
        self.game_reset = True
        self.player_0.rect.x = 64
        self.player_0.rect.y = 64
        self.player_0.death_frame = 0

        self.levels.clear()
        self.bombs.clear()
        self.bomb_ticks.clear()
        self.enemies.clear()

        for n in range(self.number_of_levels):
            path = 'data/assets/maps/level_' + str(n) + '.csv'
            level_map = TileMap(path, self.spritesheet, n)
            self.levels.append(level_map)

        self.playing = False
        self.current_menu = self.message_screen

    def get_running(self):
        return self.running

    def get_current_level(self):
        return self.current_level

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
                if event.key == pygame.K_q:
                    if self.bomb_pause is False and self.player_0.bomb_number != 0:
                        self.player_0.bomb_number -= 1
                        self.bomb_dropped = True
                    self.drop_bomb = True
                if event.key == pygame.K_u:
                    self.kill_all_enemies = True
                if event.key == pygame.K_RETURN:
                    self.enter_the_door = True
                if event.key == pygame.K_e:
                    if self.talk_to_npc is True:
                        self.talk = not self.talk
                if event.key == pygame.K_SPACE:
                    self.shoot = True
                if event.key == pygame.K_ESCAPE:
                    self.back_key = True

                # player move
                if event.key == pygame.K_RIGHT:
                    self.player_0.right_key = True
                if event.key == pygame.K_LEFT:
                    self.player_0.left_key = True
                if event.key == pygame.K_UP:
                    self.player_0.up_key = True
                if event.key == pygame.K_DOWN:
                    self.player_0.down_key = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player_0.right_key = False
                if event.key == pygame.K_LEFT:
                    self.player_0.left_key = False
                if event.key == pygame.K_UP:
                    self.player_0.up_key = False
                if event.key == pygame.K_DOWN:
                    self.player_0.down_key = False

    def reset_keys(self):
        self.click = False
        self.back_key = False
        self.drop_bomb = False
        self.shoot = False
        self.kill_all_enemies = False
        self.enter_the_door = False

    def draw_text(self, text, size, x, y, color, type='menu', font_type='regular'):
        if font_type == 'title':
            font = pygame.font.Font(self.title_font_name, size)
        else:
            font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        if type == 'game':
            self.display.blit(text_surface, text_rect)
            return text_rect
        else:
            self.menu_display.blit(text_surface, text_rect)
            return text_rect

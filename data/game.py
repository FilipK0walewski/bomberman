from data.menu import *
from data.player import Player
from data.bomb import Bomb
from data.enemy import Enemy
# from data.images import Spritesheet
# from data.npc import Npc
from data.missile import *
from data.tiles import *
from data.camera import *
from data.boss import Boss
from data.terminal import Terminal
from data.cutscene import CutSceneMenager, BossSmallTalk
from data.equipment import *


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
        self.use_key = False

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

        self.map_sheet = Spritesheet('data/assets/sprites/walls/tileset.png')
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
            level = TileMap(path, self.map_sheet, i)
            self.levels.append(level)

        self.new_level_1 = TileMap('data/assets/maps/new_level_1.csv', self.map_sheet, 1)

        # menus
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.pause_menu = PauseMenu(self)
        self.message_screen = GenerateMessage(self)
        self.current_menu = self.main_menu

        # player
        self.player_0 = Player((self.window_width, self.window_height))

        self.score = 0
        self.temp_countdown = 1000
        self.dead_tick = 0

        # camera
        self.camera = Camera(self.player_0)
        self.follow = Follow(self.camera, self.player_0)
        self.border = Border(self.camera, self.player_0)
        self.auto = Auto(self.camera, self.player_0)
        self.camera.set_method(self.follow)

        # icon ???
        icon = pygame.image.load('data/assets/sprites/cross.png')
        pygame.display.set_icon(icon)

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
        self.enemy_missiles = []

        # enemies
        self.enemies = []
        self.boss = None
        self.bosses = []

        # temp
        self.temp_variable = True

        # terminal
        self.terminal = Terminal(self.window_width, self.window_height)

        # cut scenes
        self.cut_scene_menager = CutSceneMenager(self.display, (self.window_width, self.window_height), self.font_name, self.mustard, self.background)

        # equipment
        self.backpack = Equipment((self.window_width, self.window_height), self.font_name, self.player_0)
        self.loot = []
        self.chests = []

        self.chests.append(Chest((256, 256), 0, self.player_0, (self.window_width, self.window_height)))

        for i in range(64):
            self.chests[0].add_item(Loot((0, 0), 0, 'lesser_health_potion'))

        self.chests[0].add_item(Loot((256, 256), 0, 'message', 'password: PASSWORD14'))

    def game_loop(self):
        while self.playing:
            self.check_events()

            self.update_game()
            self.draw_game()
            # fps on screen

            self.draw_text(str(round(self.clock.get_fps(), 2)), 16, 0, self.window_height / 2, self.mustard, 'game', 'bottomleft')

            self.window.blit(pygame.transform.scale(self.display, (self.window_width, self.window_height)), (0, 0))
            pygame.display.flip()
            self.clock.tick(self.FPS)
            self.reset_keys()

    def update_game(self):

        # map

        level = self.levels[self.current_level]
        map_rect = level.get_colliders()

        if len(self.enemies) == 0 and self.levels[self.current_level].map_completed is False:

            self.levels[self.current_level].map_completed = True
            self.levels[self.current_level].load_doors()

        if self.boss is not None:
            self.cut_scene_menager.start_cut_scene(BossSmallTalk(self.player_0, self.boss))

        # pause
        if self.back_key is True:
            self.current_menu = self.pause_menu
            self.playing = False

        # player
        ################################################################################################################

        self.player_0.busy = False

        if self.backpack.visible:
            self.player_0.busy = True
        else:
            self.backpack.selected = self.backpack.item_slots + 1

        if self.cut_scene_menager.cut_scene is not None:
            self.cut_scene_menager.update()

        if len(level.fog) != 0:
            for tile in level.fog:
                if abs(tile.center[0] - self.player_0.rect.center[0]) < 32:
                    self.player_0.talk = True
                else:
                    self.player_0.talk_pos = [self.player_0.rect.center[0] - self.camera.offset[0], self.player_0.rect.y - self.camera.offset[1] - 16]
                    self.player_0.talk = False

        terminals = self.levels[self.current_level].get_terminal_rect()

        if len(terminals) != 0:
            for terminal in terminals:
                temp_rect = pygame.Rect(terminal.x, terminal.y + 32, 32, 32)

                if temp_rect.colliderect(self.player_0.rect) and self.use_key is True:
                    temp = self.terminal.use
                    self.terminal.use = not temp

        if self.terminal.use is True:
            self.player_0.busy = True

        # loot

        if len(self.loot) != 0:
            for item in self.loot:
                if item.rect.colliderect(self.player_0.rect):
                    if self.use_key is True:
                        if self.backpack.empty_slots_number() != 0:
                            self.backpack.add_item(item)
                            self.loot.remove(item)
                            break
                        else:
                            print('backpack full')

        # chests

        for chest in self.chests:
            if chest.opened is True:
                self.player_0.busy = True
            if chest.rect.colliderect(self.player_0.rect):
                if self.use_key is True:
                    temp = chest.opened
                    chest.opened = not temp

        ################################################################################################################
        # camera

        self.camera.scroll()

        # missiles

        if self.shoot is True and self.player_0.busy is False:

            direction = self.player_0.direction
            missile = PlayerMissile(self.player_0.rect.topright, direction)
            self.missiles.append(missile)

        if len(self.missiles) != 0:
            for missile in self.missiles:
                for tile in map_rect:
                    if missile.rect.colliderect(tile):
                        self.missiles.remove(missile)
                        break

                for enemy in self.enemies:
                    if missile.rect.colliderect(enemy.enemy_rect):
                        enemy.take_damage(2)
                        self.missiles.remove(missile)
                        break

                missile.update()

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
                if missile.rect.colliderect(bomb.bomb_rect):
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
                        self.player_0.take_damage(10)
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
                self.player_0.take_damage(10)
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
                    # self.fade()

                    if rect[1][2] != 'i' and self.levels[self.current_level].map_completed is True:
                        temp = rect[1][1]
                        temp = int(temp)
                        if temp == self.current_level:
                            temp += 1
                        self.current_level = temp
                        self.enter_the_door_function(int(rect[1][1]))

                    else:
                        temp = rect[1][1]
                        for door in doors:
                            if door[1][1] == temp and door[0] != rect[0]:
                                self.player_0.position.x = door[0].x
                                self.player_0.position.y = door[0].y + 32
                                break
                        break

        # coins
        coins = self.levels[self.current_level].coin
        for coin in coins:
            if self.player_0.rect.colliderect(coin.rect):
                self.backpack.coins += 1
                self.player_0.coins += 1
                self.levels[self.current_level].picking(coin.rect, 'coin')

        # cheats
        if self.kill_all_enemies is True:
            self.enemies.clear()

        # npc-player

        # boss

        if self.current_level == 4:
            x, y = self.levels[self.current_level].get_level_size()
            self.boss = Boss(x, y, self.window_width, self.window_height, self.player_0.rect)

        if self.boss is not None and self.boss.defeated is False:

            self.boss.update(self.levels[self.current_level].wall, self.player_0.rect.center, 1)
            if self.boss.shoot is True and self.boss.in_cut_scene is False:
                for i in range(10):
                    temp = Missile(self.boss.rect.center, self.player_0.rect.center, 'bullet')
                    self.enemy_missiles.append(temp)
                self.boss.shoot = False

            for missile in self.enemy_missiles:

                for tile in map_rect:
                    if missile.rect.colliderect(tile):
                        self.enemy_missiles.remove(missile)
                        break

                    if missile.rect.colliderect(self.player_0.rect):
                        self.enemy_missiles.remove(missile)
                        break

                missile.update()

            x = 0
            for bomb in self.bombs:
                if self.boss.rect.colliderect(bomb.bomb_rect) and pygame.time.get_ticks() - 1000 > self.boss.damage_tick:
                    self.boss.damage_tick = pygame.time.get_ticks()
                    temp = pygame.time.get_ticks() - self.bomb_ticks[x]
                    temp = 3000 - temp
                    self.bomb_ticks[x] -= temp
                    self.boss.health -= 50
                x += 1

        # eq

        self.backpack.update()
        for item in self.loot:
            item.update(self.current_level)

        for chest in self.chests:
            chest.update(self.current_level, self.backpack)

        # terminal

        if self.terminal.use is True:
            self.terminal.update_terminal()
            if self.terminal.fans is True:
                self.levels[1] = self.new_level_1

        ################################################################################################################
        # player update

        self.player_0.update(map_rect, 1, self.cut_scene_menager)

    def draw_game(self):

        self.display.fill(self.background)

        self.levels[self.current_level].draw_map(self.camera.offset, self.display)

        # eq

        for item in self.loot:
            item.draw(self.display, self.camera.offset)

        for chest in self.chests:
            chest.draw(self.display, self.camera.offset, self.font_name)

        # bombs

        if len(self.bombs) != 0:
            for bomb in self.bombs:
                bomb.draw_bomb(self.camera.offset, self.display, self.bomb_animation)
                bomb.draw_explosion(self.camera.offset, self.display)

        for enemy in self.enemies:
            enemy.draw_enemy(self.camera.offset, self.display)

        for missile in self.missiles:
            missile.draw(self.camera.offset, self.display)

        for missile in self.enemy_missiles:
            missile.draw(self.camera.offset, self.display)

        self.player_0.draw(self.camera.offset, self.display, self.font_name)

        if self.player_0.talk is True:
            self.draw_speech(random.choice(self.player_0.quotes), self.player_0.talk_pos)

        # boss

        if self.boss is not None and self.boss.defeated is False:
            self.boss.draw_boss(self.camera.offset, self.display)
            self.boss.draw_health_bar(self.display)

        # terminal

        if self.terminal.use is True:
            self.terminal.draw_terminal(self.display)

        # backpack

        self.backpack.draw(self.display)

        # cut scenes

        self.cut_scene_menager.draw()

    def enter_the_door_function(self, spawn):

        for rect in self.levels[self.current_level].get_door_rect():
            if int(rect[1][1]) == spawn:
                self.player_0.position.x = rect[0].x
                self.player_0.position.y = rect[0].y
                if rect[2] is True:
                    self.player_0.position.y += 32
                else:
                    self.player_0.position.y += 16

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

    def game_over(self):

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

    def draw_speech(self, text, pos):

        font = pygame.font.Font(self.font_name, 16)
        text_surface = font.render(text, True, self.background)
        text_rect = text_surface.get_rect(midbottom=pos)

        # background
        bg_rect = text_rect.inflate(16, 16)
        bg_rect.bottom = pos[1] - 16
        text_rect.center = bg_rect.center

        pygame.draw.polygon(self.display, self.mustard, (pos, (pos[0] + 16, pos[1] - 16), (pos[0] - 16, pos[1] - 16)))
        pygame.draw.rect(self.display, self.mustard, bg_rect, border_radius=15)
        self.display.blit(text_surface, text_rect)

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

                # terminal

                if self.terminal.use is True:
                    self.terminal.input = event.key
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_c] and keys[pygame.K_LCTRL]:
                        print('ctrl + c')
                        self.terminal.python = False
                        self.terminal.start_line = 'ROOT:~$ '
                        self.terminal.input = 13

                # eq

                if event.key == pygame.K_TAB:
                    temp = self.backpack.visible
                    self.backpack.visible = not temp

                # game

                if event.key == pygame.K_q:
                    if self.bomb_pause is False and self.player_0.bomb_number != 0:
                        self.player_0.bomb_number -= 1
                        self.bomb_dropped = True
                    self.drop_bomb = True

                if event.key == pygame.K_u:
                    self.kill_all_enemies = True

                if event.key == pygame.K_RETURN:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.move = True
                    if self.backpack.visible is True:
                        self.backpack.use = True
                    self.enter_the_door = True

                if event.key == pygame.K_e and self.terminal.use is False:
                    if self.use_key is False:
                        self.use_key = True

                if event.key == pygame.K_SPACE:
                    self.shoot = True

                if event.key == pygame.K_ESCAPE:
                    if self.terminal.use is True:
                        self.terminal.use = False
                    else:
                        self.back_key = True

                # arrows

                if event.key == pygame.K_RIGHT:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.selected += 1
                    if self.backpack.visible is True:
                        self.backpack.selected += 1
                    self.player_0.right_key = True
                if event.key == pygame.K_LEFT:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.selected -= 1
                    if self.backpack.visible is True:
                        self.backpack.selected -= 1
                    self.player_0.left_key = True
                if event.key == pygame.K_UP:
                    if self.backpack.visible is True:
                        self.backpack.menu_position -= 1
                    self.player_0.up_key = True
                if event.key == pygame.K_DOWN:
                    if self.backpack.visible is True:
                        self.backpack.menu_position += 1
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
        self.use_key = False

    def draw_text(self, text, size, x, y, color, type='menu', pos_type='center', font_type='regular'):
        if font_type == 'title':
            font = pygame.font.Font(self.title_font_name, size)
        else:
            font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if pos_type == 'center':
            text_rect.center = (x, y)
        elif pos_type == 'bottomleft':
            text_rect.bottomleft = (x, y)

        if type == 'game':
            self.display.blit(text_surface, text_rect)
            return text_rect
        else:
            self.menu_display.blit(text_surface, text_rect)
            return text_rect

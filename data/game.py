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
import json


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
        self.drop_bomb = False
        self.shoot = False
        self.kill_all_enemies = False
        self.enter_the_door = False
        self.use_key = False

        # keys

        self.right = 1073741903
        self.left = 1073741904
        self.up = 1073741906
        self.down = 1073741905

        self.tab = 9
        self.enter = 13
        self.weapon = 32
        self.take_all = 97
        self.use = 101
        self.q = 113

        # screen
        self.json_path = 'startup.json'
        with open(self.json_path) as f:
            self.json_data = json.load(f)
        f.close()

        self.window_width = self.json_data['screen']['resolution']['width']
        self.window_height = self.json_data['screen']['resolution']['height']

        if self.json_data['screen']['fullscreen'] == 'on':
            self.window = pygame.display.set_mode((self.window_width, self.window_height), pygame.FULLSCREEN)
            self.full_screen = 'on'
        else:
            self.window = pygame.display.set_mode((self.window_width, self.window_height))
            self.full_screen = 'off'

        self.FPS = self.json_data['screen']['fps']
        self.ray_tracing = self.json_data['screen']['ray_tracing']
        self.go_to_fps = 60
        self.delta_time = 0

        self.display = pygame.Surface((int(self.window_width / 2), int(self.window_height / 2)))
        self.menu_display = pygame.Surface((int(self.window_width), int(self.window_height)))

        pygame.display.set_caption('Bomberman Simulator 2D RPG')

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
            name = "bug_" + str(n)
            self.bug_animation.append(bug_animation_sheet.parse_sprite(name))

        number_of_images = 5

        for n in range(number_of_images):
            name = "bomb_" + str(n)
            self.bomb_animation.append(self.spritesheet.parse_sprite(name))

        # maps
        self.number_of_levels = 7

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

        self.videos = VideosMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)

        self.current_menu = self.main_menu

        # player
        self.player_0 = Player((self.window_width, self.window_height))

        # camera
        self.camera = Camera(self.player_0)
        self.follow = Follow(self.camera, self.player_0)
        self.border = Border(self.camera, self.player_0)
        self.auto = Auto(self.camera, self.player_0)
        self.camera.set_method(self.follow)

        # icon ???
        icon = pygame.image.load('data/assets/sprites/enemy/boss_miniature.png')
        pygame.display.set_icon(icon)

        # NPCs
        # self.npc_0 = Npc(self.levels[0].get_spawn_rect(), self)
        self.talk_to_npc = False

        # bombs
        self.bomb_dropped = False
        self.bomb_pause = True
        self.bombs = []
        self.old_bombs = []
        self.bomb_rect = []
        self.explosion_length = 1
        self.last_explosion_tick = 0

        # missiles
        self.missiles = []
        self.enemy_missiles = []

        # enemies
        self.enemies = []
        self.boss = None
        self.bosses = []
        self.turn_rect = []
        self.spawn_rect = self.levels[0].get_spawn_rect()

        # terminal
        self.terminal = Terminal(self.window_width, self.window_height)

        # cut scenes
        self.cut_scene_menager = CutSceneMenager(self.display, (self.window_width, self.window_height), self.font_name, self.mustard, self.background)

        # equipment
        self.backpack = Equipment((self.window_width, self.window_height), self.font_name, self.player_0)
        self.loot = []
        self.chests = []
        self.spawn_loot()

    def spawn_loot(self):

        self.chests.append(Chest((360, 64), 0, self.player_0, (self.window_width, self.window_height)))

        pos = (self.levels[4].map_w / 2, self.levels[4].map_h / 2)
        self.loot.append(Loot(pos, 4, 'message', 'password to terminal: PASSWORD14'))
        self.loot.append(Loot((128, -128), 6, 'message', 'more soon, quit the game'))

        for i in range(64):
            self.chests[0].add_item(Loot((0, 0), 0, 'lesser_health_potion'))

        for i in range(256):
            self.chests[0].add_item(Loot((0, 0), 0, 'bomb', 'very dangerous'))

        self.chests[0].add_item(Loot((0, 0), 0, 'message', 'q=drop bomb, a=take all, space=shoot'))

    def game_loop(self):
        while self.playing:

            self.check_events()
            self.update_game()
            self.draw_game()

            # fps on screen
            self.draw_text(str(round(self.clock.get_fps(), 2)), 16, (0, self.window_height / 2), self.mustard, 'game', 'bottomleft')
            self.window.blit(pygame.transform.scale(self.display, (self.window_width, self.window_height)), (0, 0))
            pygame.display.flip()

            self.delta_time = self.clock.tick(self.FPS) * .001 * self.go_to_fps
            self.reset_keys()

    def update_game(self):

        # map

        level = self.levels[self.current_level]
        map_rect = level.get_colliders()

        if self.boss is not None:
            self.cut_scene_menager.start_cut_scene(BossSmallTalk(self.player_0, self.boss))
            if self.boss.defeated is False:
                self.levels[self.current_level].map_completed = False
                self.levels[self.current_level].load_doors()

        if len(self.enemies) == 0 and self.levels[self.current_level].map_completed is False:
            self.levels[self.current_level].map_completed = True
            self.levels[self.current_level].load_doors()

        # pause
        if self.back_key is True:
            self.current_menu = self.pause_menu
            self.playing = False

        # colors
        self.player_0.img_color = (255, 255, 255)
        if self.boss is not None:
            self.boss.img_color = (255, 255, 255)

        for enemy in self.enemies:
            if enemy.type == 'mutant':
                enemy.color = self.magenta

        # player
        ################################################################################################################

        self.player_0.busy = False

        if self.backpack.visible:
            self.player_0.busy = True
        else:
            self.backpack.selected = self.backpack.item_slots + 1

        if self.cut_scene_menager.cut_scene is not None:
            self.cut_scene_menager.update(self.delta_time, self.shoot)

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
        tick = pygame.time.get_ticks()
        if self.shoot is True and tick - 500 > self.player_0.shoot_delay:

            direction = self.player_0.direction
            missile = PlayerMissile(self.player_0.rect.topright, direction)
            self.missiles.append(missile)

        for missile in self.missiles:
            for tile in map_rect:
                if missile.rect.colliderect(tile):
                    self.missiles.remove(missile)
                    break

            for enemy in self.enemies:
                if missile.rect.colliderect(enemy.rect):
                    enemy.take_damage(10)
                    if missile in self.missiles:
                        self.missiles.remove(missile)
                        break

            if self.boss is not None:
                if self.boss.rect.collidepoint(missile.center):
                    self.boss.take_damage(3)
                    self.missiles.remove(missile)

            missile.update(self.delta_time)

        for missile in self.enemy_missiles:

            if missile.rect.colliderect(self.player_0.rect):
                self.player_0.take_damage(10)
                self.player_0.img_color = self.magenta
                self.enemy_missiles.remove(missile)

            for tile in map_rect:
                if missile.rect.colliderect(tile):
                    self.enemy_missiles.remove(missile)
                    break

            missile.update(self.delta_time)

        # bomb
        if self.bomb_dropped is True:
            bomb_info = []
            current_tick = pygame.time.get_ticks()

            bomb = Bomb(self.player_0.rect, self.levels[self.current_level].get_hard_wall(),
                        self.levels[self.current_level].get_soft_wall(), self.explosion_length)
            self.bomb_rect.append(bomb.bomb_rect)
            bomb.move_bomb(map_rect)

            bomb_info.append(bomb)
            bomb_info.append(current_tick)
            self.bombs.append(bomb_info)

            self.bomb_pause = True
            self.bomb_dropped = False
            self.player_0.on_bomb = True

            for enemy in self.enemies:
                if enemy.rect.colliderect(bomb.bomb_rect):
                    enemy.on_bomb = True

        if len(self.bombs) != 0:
            if self.bomb_pause is True and pygame.time.get_ticks() - self.bombs[-1][1] > 100:
                self.bomb_pause = False
        else:
            self.bomb_pause = False

        temp = 0
        for bomb in self.bomb_rect:
            if bomb.colliderect(self.player_0.rect):
                temp += 1

        if temp == 0:
            self.player_0.on_bomb = False

        for bomb in self.bombs:
            for missile in self.missiles:
                if bomb not in self.old_bombs:
                    if missile.rect.colliderect(bomb[0].bomb_rect):
                        temp = pygame.time.get_ticks() - bomb[1]
                        temp = 3000 - temp
                        bomb[1] -= temp
                        self.old_bombs.append(bomb)
                        self.missiles.remove(missile)
                        break
            for missile in self.enemy_missiles:
                if bomb not in self.old_bombs:
                    if missile.rect.colliderect(bomb[0].bomb_rect):
                        temp = pygame.time.get_ticks() - bomb[1]
                        temp = 3000 - temp
                        bomb[1] -= temp
                        self.old_bombs.append(bomb)
                        self.enemy_missiles.remove(missile)
                        break
            if bomb not in self.old_bombs and self.boss is not None:
                if self.boss.rect.colliderect(bomb[0].bomb_rect):
                    temp = pygame.time.get_ticks() - bomb[1]
                    temp = 3000 - temp
                    bomb[1] -= temp
                    self.old_bombs.append(bomb)

        # removing bombs
        tick = pygame.time.get_ticks()
        help_variable = 0
        for bomb in self.bombs:
            if tick - bomb[1] >= 3000:

                self.bombs[help_variable][0].explosion()
                self.bombs[help_variable][0].find_edges()

                explosion_rect = self.bombs[help_variable][0].explosion_rect
                new_turns = self.levels[self.current_level].wall_destroying(explosion_rect)

                for rect in new_turns:
                    self.turn_rect.append(rect)

                # player, enemy dmg
                for tile in explosion_rect:
                    for enemy in self.enemies:
                        if enemy.rect.collidepoint(tile.center):
                            enemy.take_damage(100)
                            if enemy.type == 'mutant':
                                enemy.color = self.mustard
                    if tile.colliderect(self.player_0.rect):
                        self.player_0.take_damage(20)
                        self.player_0.img_color = self.magenta
                    if self.boss is not None:
                        if self.boss.rect.collidepoint(tile.center) and pygame.time.get_ticks() - 1000 > self.boss.damage_tick:
                            self.boss.take_damage(20)
                            self.boss.img_color = self.magenta
                            if self.boss.max_health > self.boss.current_health * 2:
                                self.boss.radius -= 3

                    for inner_bomb in self.bombs:
                        if inner_bomb != bomb and inner_bomb not in self.old_bombs:
                            if tile.colliderect(inner_bomb[0].bomb_rect):
                                temp = pygame.time.get_ticks() - inner_bomb[1]
                                temp = 3000 - temp
                                inner_bomb[1] -= temp
                                self.old_bombs.append(bomb)

                if len(self.bombs) == 1 and len(self.old_bombs) == 1:
                    pass
                    # self.bombs[0][1] = self.old_bombs[-1][1]

                if pygame.time.get_ticks() - bomb[1] >= 3490:
                    self.bombs.pop(help_variable)
                    self.bomb_rect.pop(help_variable)
            help_variable += 1

        if len(self.bombs) == 0:
            self.old_bombs = []
            self.bomb_rect = []

        # enemies

        for enemy in self.enemies:
            if enemy.enemy_hp > 0:
                if enemy.rect.collidelistall(self.bomb_rect):
                    pass
                else:
                    enemy.on_bomb = False
                if abs(enemy.rect.x - self.player_0.rect.x) <= self.window_width / 4 + 50:
                    if abs(enemy.rect.y - self.player_0.rect.y) <= self.window_height / 4 + 50:
                        enemy.update(map_rect, self.bomb_rect, self.turn_rect, self.player_0.rect.center, self.delta_time)
            if enemy.rect.colliderect(self.player_0.rect):
                self.player_0.take_damage(20)
                self.player_0.img_color = self.magenta
            if enemy.to_remove is True:
                self.player_0.gain_xp(10)
                self.enemies.remove(enemy)
            if enemy.rect.x < 0 or enemy.rect.y < 0 or enemy.rect.x > level.get_level_size()[0] or enemy.rect.y > level.get_level_size()[1]:
                enemy.take_damage(100000)

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

        # boss

        if self.current_level == 4 and len(self.loot) == 1 and self.boss is None:
            x, y = self.levels[self.current_level].get_level_size()
            self.boss = Boss(x, self.window_width, self.window_height, self.player_0.rect)

        if self.boss is not None and self.boss.defeated is False:

            if self.boss.rect.colliderect(self.player_0.rect):
                self.player_0.take_damage(25)
                self.player_0.img_color = self.magenta

            self.boss.update(self.player_0.rect.center, self.bomb_rect, self.delta_time)
            if self.boss.shoot is True and self.boss.in_cut_scene is False:
                temp = Missile(self.boss.rect.center, self.player_0.rect.center, 'bullet')
                self.enemy_missiles.append(temp)
                self.boss.shoot = False

        # eq

        self.backpack.update(self.player_0, self.delta_time)
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
        if self.player_0.on_bomb is True:
            self.player_0.update(map_rect, self.delta_time, self.cut_scene_menager)
        else:
            temp = map_rect.copy()
            for bomb in self.bomb_rect:
                temp.append(bomb)
            self.player_0.update(temp, self.delta_time, self.cut_scene_menager)

        if self.player_0.current_health <= 0:
            self.playing = False
            self.current_menu = self.message_screen

    def draw_game(self):

        self.display.fill(self.background)

        self.levels[self.current_level].draw_map(self.camera.offset, self.display)

        '''
        for rect in self.turn_rect:
            temp = (rect.x - self.camera.offset.x, rect.y - self.camera.offset.y, 32, 32)
            pygame.draw.rect(self.display, (0, 64, 0, 32), temp)
        '''
        # eq

        for item in self.loot:
            item.draw(self.display, self.camera.offset)

        for chest in self.chests:
            chest.draw(self.display, self.camera.offset, self.font_name)

        # bombs

        if len(self.bombs) != 0:
            for bomb in self.bombs:
                bomb[0].draw_bomb(self.camera.offset, self.display, self.bomb_animation)
                bomb[0].draw_explosion(self.camera.offset, self.display)

        for enemy in self.enemies:
            if abs(enemy.rect.x - self.player_0.rect.x) <= self.window_width / 4 + 100:
                if abs(enemy.rect.y - self.player_0.rect.y) <= self.window_height / 4 + 100:
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
        if self.cut_scene_menager.cut_scene is not None:
            self.cut_scene_menager.draw()

    def enter_the_door_function(self, spawn):

        for rect in self.levels[self.current_level].get_door_rect():
            if int(rect[1][1]) == spawn:
                self.player_0.position.x = rect[0].x
                self.player_0.position.y = rect[0].y
                if rect[2] is True:
                    self.player_0.position.y += 32
                else:
                    self.player_0.position.y -= 16

        self.bomb_pause = True

        self.bombs = []
        self.enemies = []
        self.turn_rect.clear()
        self.turn_rect = self.levels[self.current_level].get_turn_rect()

        n = len(self.levels[self.current_level].floor) / 20
        if self.levels[self.current_level].map_completed is False and self.levels[self.current_level].without_enemies is False:
            for n in range(int(n)):
                enemy = Enemy(self.levels[self.current_level].get_spawn_rect(), self.bug_animation, self.death_animation)
                self.enemies.append(enemy)
            for n in range((self.current_level - 1)**3):
                enemy = Enemy(self.levels[self.current_level].get_spawn_rect(), self.bug_animation, self.death_animation,
                              'mutant')
                self.enemies.append(enemy)

    def game_over(self, reset=False):

        self.player_0 = Player((self.window_width, self.window_height))
        self.current_level = 0
        self.levels = []
        for i in range(self.number_of_levels):
            path = 'data/assets/maps/level_' + str(i) + '.csv'
            level = TileMap(path, self.map_sheet, i)
            self.levels.append(level)
        self.new_level_1 = TileMap('data/assets/maps/new_level_1.csv', self.map_sheet, 1)

        self.bomb_dropped = False
        self.bomb_pause = True
        self.bombs = []
        self.old_bombs = []
        self.bomb_rect = []
        self.explosion_length = 1
        self.turn_rect = []

        self.missiles = []
        self.enemy_missiles = []

        self.enemies = []
        self.boss = None
        self.bosses = []

        self.terminal = Terminal(self.window_width, self.window_height)
        self.cut_scene_menager = CutSceneMenager(self.display, (self.window_width, self.window_height), self.font_name,
                                                 self.mustard, self.background)

        self.backpack = Equipment((self.window_width, self.window_height), self.font_name, self.player_0)
        self.loot = []
        self.chests = []
        self.spawn_loot()

        self.camera = Camera(self.player_0)
        self.follow = Follow(self.camera, self.player_0)
        self.border = Border(self.camera, self.player_0)
        self.auto = Auto(self.camera, self.player_0)
        self.camera.set_method(self.follow)
        self.last_explosion_tick = 0

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
                        self.terminal.python = False
                        self.terminal.start_line = 'ROOT:~$ '
                        self.terminal.input = 13

                # eq

                if event.key == self.tab:
                    temp = self.backpack.visible
                    self.backpack.visible = not temp

                # game

                if event.key == self.q:
                    if self.bomb_pause is False and self.backpack.bomb_number != 0:
                        for item in self.backpack.items:
                            if item.type == 'bomb':
                                item.stored -= 1
                                break
                        self.bomb_dropped = True
                    self.drop_bomb = True

                if event.key == pygame.K_u:
                    self.kill_all_enemies = True

                if event.key == 97:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.move_all = True

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

                if event.key == self.right:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.selected += 1
                    if self.backpack.visible is True:
                        self.backpack.selected += 1
                    self.player_0.right_key = True
                if event.key == self.left:
                    for chest in self.chests:
                        if chest.opened is True:
                            chest.selected -= 1
                    if self.backpack.visible is True:
                        self.backpack.selected -= 1
                    self.player_0.left_key = True
                if event.key == self.up:
                    if self.backpack.visible is True:
                        self.backpack.menu_position -= 1
                    self.player_0.up_key = True
                if event.key == self.down:
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

    def draw_text(self, text, size, pos, color, type='menu', pos_type='center', asci=False, font_type='regular'):
        if font_type == 'title':
            font = pygame.font.Font(self.title_font_name, size)
        else:
            font = pygame.font.Font(self.font_name, size)

        if asci is True:
            temp = text
            if temp == 1073741903:
                text = 'right'
            elif temp == 1073741904:
                text = 'left'
            elif temp == 1073741905:
                text = 'down'
            elif temp == 1073741906:
                text = 'up'
            elif temp == 9:
                text = 'tab'
            elif temp == 13:
                text = 'enter'
            elif temp == 32:
                text = 'space'
            else:
                text = chr(temp)

        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()

        if pos_type == 'center':
            text_rect.center = pos
        elif pos_type == 'bottomleft':
            text_rect.bottomleft = pos
        elif pos_type == 'topright':
            text_rect.topright = pos
        elif pos_type == 'topleft':
            text_rect.topleft = pos

        if type == 'game':
            self.display.blit(text_surface, text_rect)
            return text_rect
        else:
            self.menu_display.blit(text_surface, text_rect)
            return text_rect

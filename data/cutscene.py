import pygame
from data.images import Spritesheet


def draw_text(pos, text, display, font, color):
    font = pygame.font.Font(font, 16)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = pos
    display.blit(text_surface, text_rect)


class CutScene0:

    def __init__(self, player):

        self.player = player

        self.name = 'game_beginning'
        self.timer = pygame.time.get_ticks()
        self.running = True
        self.talk = True

        self.quotes = ['FILIP KOWALEWSKI', '...', "LET'S GO"]
        self.quote_number = 0
        self.quotation_counter = 0

    def update(self):
        self.player.in_cutscene = True
        temp_timer = pygame.time.get_ticks()

        if temp_timer - 250 > self.timer:
            keys = pygame.key.get_pressed()
            space = keys[pygame.K_SPACE]
        else:
            space = 0

        if int(self.quotation_counter) < len(self.quotes[self.quote_number]):
            self.quotation_counter += .1
            if space:
                self.timer = temp_timer
                self.quotation_counter = len(self.quotes[self.quote_number])
        else:
            if space:
                self.timer = temp_timer
                if self.quote_number == len(self.quotes) - 1:
                    self.running = False
                    self.player.in_cutscene = False
                    self.talk = False
                else:
                    if int(self.quotation_counter) == len(self.quotes[self.quote_number]):
                        self.quote_number += 1
                        self.quotation_counter = 0

    def draw(self, display, font, color, pos):
            n = int(self.quotation_counter)
            draw_text((pos[0] / 2, pos[1] / 8), self.quotes[self.quote_number][0:n], display, font, color)


class BossSmallTalk:

    def __init__(self, player, boss):
        self.name = 'boss_small_talk_before_fight'
        self.timer = 0
        self.running = True
        self.talk = False

        self.player = player
        self.boss = boss

        self.phase = 0
        self.boss_quotes = ['HA HA HA', 'HA HA HA HA', 'HA HA']
        self.player_quotes = ['OH NO', 'HERE WE GO AGAIN...']
        self.display_quote = ''

        self.quote_number = 0
        self.quotation_counter = 0
        self.dialogue = 0

        boss_sheet = Spritesheet('data/assets/sprites/enemy/boss_0_talk.png')
        player_sheet = Spritesheet('data/assets/sprites/player_talk.png')

        self.boss_anim = []
        self.player_anim = []
        self.anim_pos = (0, 0)
        self.anim_tick = 100

        for i in range(6):
            name = 'boss_talk_' + str(i)
            self.boss_anim.append(boss_sheet.parse_sprite(name))
            name = 'player_talk_' + str(i)
            self.player_anim.append(player_sheet.parse_sprite(name))

        self.image = self.boss_anim[0]
        self.frame = 0

    def update(self):

        temp_timer = pygame.time.get_ticks()

        if temp_timer - 500 > self.timer:
            keys = pygame.key.get_pressed()
            space = keys[pygame.K_SPACE]
        else:
            space = 0

        if self.phase == 0:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True
            if abs(self.boss.rect.center[0] - self.player.rect.center[0]) > 128:
                self.boss.position.x += 1
            else:
                self.talk = True
                self.phase += 1

        if self.phase == 1:
            if self.dialogue % 2 == 0:
                self.display_quote = self.boss_quotes[self.quote_number]
                self.image = self.boss_anim[self.frame]

            else:
                self.image = self.player_anim[self.frame]
                if self.quote_number == len(self.player_quotes):
                    self.phase += 1
                else:
                    self.display_quote = self.player_quotes[self.quote_number]

            if temp_timer - 100 > self.anim_tick:
                self.anim_tick = temp_timer
                self.frame = (self.frame + 1) % len(self.boss_anim)

            if int(self.quotation_counter) < len(self.display_quote):
                self.quotation_counter += .1
                if space:
                    self.timer = temp_timer
                    self.quotation_counter = len(self.display_quote)
            else:
                if space:
                    self.timer = temp_timer
                    self.quotation_counter = 0
                    self.dialogue += 1
                    if self.dialogue % 2 == 0:
                        self.quote_number += 1
                    self.frame = 0

        if self.phase == 2:
            self.boss.in_cut_scene = False
            self.player.in_cutscene = False
            self.talk = False

            if self.boss.max_health > 2 * self.boss.health:
                self.phase += 1

        if self.phase == 3:

            self.player.in_cutscene = True
            if abs(self.boss.rect.center[0] - self.player.rect.center[0]) > 128:
                self.quotation_counter = 0
            else:
                self.boss.in_cut_scene = True
                self.talk = True
                self.dialogue = 0
                self.display_quote = self.boss_quotes[0]
                self.image = self.boss_anim[self.frame]

                if int(self.quotation_counter) < len(self.display_quote):
                    self.quotation_counter += .1

                if temp_timer - 100 > self.anim_tick:
                    self.anim_tick = temp_timer
                    self.frame = (self.frame + 1) % len(self.boss_anim)

                if space:
                    self.boss.go_to_pos.x = 2000
                    self.phase += 1

        if self.phase == 4:
            self.boss.in_cut_scene = False
            self.player.in_cutscene = False
            self.talk = False

            if self.boss.max_health > 8 * self.boss.health:
                self.phase += 1

        if self.phase == 5:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True
            if abs(self.boss.rect.center[0] - self.player.rect.center[0]) > 128:
                self.boss.position.x += 1
                self.quotation_counter = 0
            else:
                self.talk = True
                self.dialogue = 0
                self.display_quote = 'I WILL BE BACK'
                self.image = self.boss_anim[self.frame]

                if int(self.quotation_counter) < len(self.display_quote):
                    self.quotation_counter += .1

                if temp_timer - 100 > self.anim_tick:
                    self.anim_tick = temp_timer
                    self.frame = (self.frame + 1) % len(self.boss_anim)

                if space:
                    self.talk = False
                    self.player.in_cutscene = False
                    self.boss.in_cut_scene = False
                    self.running = False

                    self.boss.defeated = True

    def draw(self, display, font, color, pos):
        if self.talk is True:
            n = int(self.quotation_counter)
            draw_text((pos[0] / 2, pos[1] / 8), self.display_quote[0:n], display, font, color)

            if self.dialogue % 2 == 0:
                display.blit(self.image, (pos[0] / 4, pos[1] / 8 - 16))
            else:
                display.blit(self.image, (3 * pos[0] / 4, pos[1] / 8 - 16))


class CutSceneMenager:

    def __init__(self, display, window_size, font, color, bg_color):
        self.cut_scenes_completed = []
        self.cut_scene = None
        self.cut_scene_running = False

        self.display = display
        self.font = font
        self.color = color
        self.bg_color = bg_color
        self.window_w = window_size[0] / 2
        self.window_h = window_size[1] / 2

        self.window_pos = -self.display.get_height() * .25

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_completed:
            self.cut_scenes_completed.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.window_pos = -self.display.get_height() * .25
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):
        if self.cut_scene_running:
            if self.window_pos < 0 and self.cut_scene.talk is True:
                self.window_pos += 1
            else:
                self.cut_scene.update()

            if self.cut_scene.talk is False and self.window_pos > -self.display.get_height() * .25:
                self.window_pos -= 5
            self.cut_scene_running = self.cut_scene.running
        else:
            self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            if self.window_pos != self.display.get_height() * .25:
                pygame.draw.rect(self.display, self.bg_color, (0, self.window_pos, self.window_w, self.display.get_height() * .25), border_radius=15)
                pygame.draw.rect(self.display, self.color, (0, self.window_pos, self.window_w, self.display.get_height() * .25), 10, border_radius=15)

            self.cut_scene.draw(self.display, self.font, self.color, (self.window_w, self.window_h))

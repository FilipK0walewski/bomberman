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
        self.player.in_cutscene = True

        self.name = 'game_beginning'
        self.timer = pygame.time.get_ticks()
        self.running = True
        self.talk = True

        self.quotes = ['Press space', 'Watch out fot cockroaches', 'ogunie', 'ben ben']
        self.quote_number = 0
        self.quotation_counter = 0

    def update(self, dt, space):

        if int(self.quotation_counter) < len(self.quotes[self.quote_number]):
            self.quotation_counter += .1 * dt
            if space:
                self.quotation_counter = len(self.quotes[self.quote_number])
        else:
            if space:
                if self.quote_number == len(self.quotes) - 1:
                    self.running = False
                    self.player.in_cutscene = False
                    self.talk = False
                else:
                    if int(self.quotation_counter) == len(self.quotes[self.quote_number]):
                        self.quote_number += 1
                        self.quotation_counter = 0

    def draw(self, display, font, color, rect):
            n = int(self.quotation_counter)
            draw_text(rect.center, self.quotes[self.quote_number][0:n], display, font, color)


class BossSmallTalk:

    def __init__(self, player, boss):
        self.name = 'boss_small_talk_before_fight'
        self.timer = 0
        self.running = True
        self.talk = False

        self.player = player
        self.boss = boss

        self.phase = 0
        self.boss_quotes = ['HA HA HA', 'AAAAAAAAAAAAAAAAAAAAAA', 'HA HA']
        self.player_quotes = ['KAROL?', 'HERE WE GO AGAIN...']
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

    def update(self, dt, space):

        temp_timer = pygame.time.get_ticks()

        if self.phase == 0:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True

            if abs(self.boss.rect.center[0] - self.player.rect.center[0]) > 128:
                self.boss.position.x += 2 * dt
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
                self.quotation_counter += .1 * dt
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

            if self.boss.max_health > 2 * self.boss.current_health:
                self.phase += 1

        if self.phase == 3:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True
            difference = self.boss.rect.center[0] - self.player.rect.center[0]
            if abs(difference) > 128:
                self.boss.position.x -= difference * .1
                self.quotation_counter = 0
            else:
                self.talk = True
                self.dialogue = 0
                self.boss.img_color = (255, 0, 32)
                self.display_quote = "I'M ANGRY !!!"
                self.image = self.boss_anim[self.frame]

                if int(self.quotation_counter) < len(self.display_quote):
                    self.quotation_counter += .1

                if temp_timer - 100 > self.anim_tick:
                    self.anim_tick = temp_timer
                    self.frame = (self.frame + 1) % len(self.boss_anim)

                if space:
                    self.boss.vector.x = self.boss.window_w / 32
                    self.boss.vector.y = 0
                    self.boss.angle = 180
                    self.phase += 1

        if self.phase == 4:

            self.boss.img_color = (255, 0, 32)
            self.boss.in_cut_scene = False
            self.player.in_cutscene = False
            self.talk = False

            if self.boss.max_health > 8 * self.boss.current_health:
                self.phase += 1

        if self.phase == 5:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True
            difference = self.boss.rect.center[0] - self.player.rect.center[0]
            if abs(difference) > 128:
                self.boss.position.x -= difference * .1
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
                    self.boss.vector.x = self.boss.window_w / 16
                    self.boss.vector.y = 0
                    self.boss.angle = 90
                    self.phase += 1

        if self.phase == 6:
            self.boss.in_cut_scene = True
            self.player.in_cutscene = True
            self.talk = False
            self.boss.angle = 90

            if abs(self.boss.rect.center[0] - self.player.rect.center[0]) < 1024:
                self.boss.position.x -= 4 * dt
            else:
                self.boss.in_cut_scene = False
                self.player.in_cutscene = False
                self.running = False
                self.boss.defeated = True

    def draw(self, display, font, color, rect):
        if self.talk is True:
            n = int(self.quotation_counter)
            draw_text(rect.center, self.display_quote[0:n], display, font, color)

            if self.dialogue % 2 == 0:
                display.blit(self.image, (rect.center[0] * .5, (rect.center[1] + self.image.get_width()) * .5))
            else:
                display.blit(self.image, (rect.center[0] * 1.5, (rect.center[1] + self.image.get_width()) * .5))


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

        self.bg_rect = pygame.Rect(0, -self.window_h / 4, self.window_w, self.window_h / 4)

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_completed:
            self.cut_scenes_completed.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):

        self.cut_scene = None
        self.cut_scene_running = False

    def update(self, dt, space):
        if self.cut_scene_running:
            if self.bg_rect.y < 0 and self.cut_scene.talk is True:
                if dt < 50:
                    self.bg_rect.y += 3 * dt
            else:
                self.cut_scene.update(dt, space)

            if self.cut_scene.talk is False and self.bg_rect.y + self.bg_rect.height > 0:
                self.bg_rect.y -= 5 * dt
            self.cut_scene_running = self.cut_scene.running
        else:
            if self.bg_rect.y + self.bg_rect.height > 0:
                self.bg_rect.y -= 3 * dt
            else:
                self.end_cut_scene()

    def draw(self):
        if self.bg_rect.y + self.bg_rect.height > 0:
            if self.bg_rect.y != self.display.get_height() * .25:
                pygame.draw.rect(self.display, self.bg_color, self.bg_rect, border_radius=15)
                pygame.draw.rect(self.display, self.color, self.bg_rect, 10, border_radius=15)

            self.cut_scene.draw(self.display, self.font, self.color, self.bg_rect)

import pygame
import random


class Npc:
    def __init__(self, spawn, game):
        self.spawn = spawn
        self.game = game
        self.i = 0
        self.shopping = False
        self.not_enough_money = False

        self.font_size = 20
        self.mid_w = self.game.window_width / 4
        self.mid_h = self.game.window_height / 4
        self.font_color = self.game.mustard
        self.arrow_color = self.game.mustard
        self.b_color = self.game.mustard
        self.med_color = self.game.mustard
        self.bomb_color = self.game.mustard
        self.upgrade_color = self.game.mustard

        rand = random.choice(spawn)
        self.npc_rect = pygame.Rect(rand.x, rand.y, 32, 32)

        self.talk_rect = [pygame.Rect(self.npc_rect.x, self.npc_rect.y, 32, 32),
                          pygame.Rect(self.npc_rect.x, self.npc_rect.y, 32, 32),
                          pygame.Rect(self.npc_rect.x, self.npc_rect.y + 16, 32, 32),
                          pygame.Rect(self.npc_rect.x, self.npc_rect.y - 16, 32, 32)]

        self.npc_image = pygame.image.load('data/assets/sprites/axe.png')
        self.dialog = ["oh",
                       "howdy",
                       "wanna buy something?"]

        self.menu_rect = pygame.Rect(0, 0, self.mid_w + 100, self.mid_h - 50)
        self.menu_rect.center = (self.mid_w, self.mid_h)
        self.menu_rect.y += 105
        self.buttons = []

    def draw_npc(self, s, display):
        display.blit(self.npc_image, (self.npc_rect.x - 4 - s[0], self.npc_rect.y - s[1]))

    def draw_chat(self, display):
        pygame.draw.rect(display, self.game.mustard, (self.menu_rect.x - 5, self.menu_rect.y - 5, self.mid_w + 110, self.mid_h - 40))
        pygame.draw.rect(display, self.game.background, self.menu_rect)

        mx, my = pygame.mouse.get_pos()
        mx = mx / 2
        my = my / 2

        if self.game.player_0.coins < 10:
            self.not_enough_money = True
        else:
            self.not_enough_money = False

        if self.shopping is False:
            self.game.draw_text("JANUSZ: " + self.dialog[self.i], self.font_size, self.mid_w, self.mid_h + 100, self.game.mustard, type='game')
            rect = self.game.draw_text('>', self.font_size, self.mid_w, self.mid_h + 120, self.arrow_color, type='game')

            if rect.collidepoint(mx, my):
                self.arrow_color = self.game.white
                if self.game.click is True:
                    self.i += 1
                    if self.i == len(self.dialog):
                        self.shopping = True
            else:
                self.arrow_color = self.game.mustard
        elif self.shopping is True and self.not_enough_money is False:
            self.buttons = []
            b_upgrade = self.game.draw_text('BOMB UPGRADE', self.font_size, self.mid_w, self.mid_h + 20 + 105, self.upgrade_color, type='game')
            b_bomb = self.game.draw_text('BOMB', self.font_size, self.mid_w, self.mid_h + 105, self.bomb_color, type='game')
            b_med = self.game.draw_text('MED KIT', self.font_size, self.mid_w, self.mid_h - 20 + 105, self.med_color, type='game')
            b_rect = self.game.draw_text('BYE', self.font_size, self.mid_w, self.mid_h + 50 + 105, self.b_color, type='game')

            if b_rect.collidepoint(mx, my):
                self.b_color = self.game.white
                if self.game.click is True:
                        self.game.talk = False
                        self.shopping = False
                        self.i = 0
            else:
                self.b_color = self.game.mustard

            if b_upgrade.collidepoint(mx, my):
                self.upgrade_color = self.game.white
                if self.game.click is True:
                    if self.not_enough_money is True:
                        print("not enough money")
                    else:
                        self.game.player_0.coins -= 10
                        self.game.explosion_length += 1
            else:
                self.upgrade_color = self.game.mustard

            if b_bomb.collidepoint(mx, my):
                self.bomb_color = self.game.white
                if self.game.click is True:
                    if self.not_enough_money is True:
                        pass
                    else:
                        self.game.player_0.coins -= 10
                        self.game.player_0.bomb_number += 1
            else:
                self.bomb_color = self.game.mustard

            if b_med.collidepoint(mx, my):
                self.med_color = self.game.white
                if self.game.click is True:
                    self.game.player_0.coins -= 10
                    self.game.player_0.player_hearts += 1
            else:
                self.med_color = self.game.mustard

        else:
            self.game.draw_text('JANUSZ: YOU ARE TOO POOR', self.font_size, self.mid_w, self.mid_h + 105, self.bomb_color, type='game')
            b_rect = self.game.draw_text('BYE', self.font_size, self.mid_w, self.mid_h + 50 + 105, self.b_color,
                                         type='game')
            if b_rect.collidepoint(mx, my):
                self.b_color = self.game.white
                if self.game.click is True:
                        self.game.talk = False
                        self.shopping = False
                        self.i = 0
            else:
                self.b_color = self.game.mustard

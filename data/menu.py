import pygame
import random
from data.bomb import Bomb


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.window_width / 2
        self.mid_h = self.game.window_height / 2
        self.run_display = True
        self.run_animation = True
        self.temp_tick = 500
        self.y_spawn = - 32
        self.falling_bombs = []
        self.mx, self.my = 0, 0
        self.cross_img = pygame.image.load('data/assets/sprites/cross.png')
        self.cross_img = pygame.transform.scale(self.cross_img, (50, 70))
        self.first_start = True

    def screen_blit(self):
        self.game.window.blit(self.game.menu_display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def menu_animation(self):
        tick = pygame.time.get_ticks()
        if tick - self.temp_tick >= 500:
            self.temp_tick = pygame.time.get_ticks()
            x_spawn = random.randint(0, self.game.window_width - 32)
            falling_bomb_rect = pygame.Rect(x_spawn, self.y_spawn, 32, 32)
            bomb = Bomb(falling_bomb_rect, [], [], 1)
            self.falling_bombs.append(bomb)

        for bomb in self.falling_bombs:
            bomb.bomb_falling(self.game.menu_display, self.game.bomb_animation[0])

            if bomb.bomb_rect.collidepoint(self.mx, self.my):
                if self.game.click:
                    bomb.explosion()
                    self.falling_bombs.remove(bomb)

            if bomb.bomb_rect.y >= self.mid_h * 2 + 32:
                self.falling_bombs.remove(bomb)


class GenerateMessage(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.level_x, self.level_y = self.mid_w, self.mid_h

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            if self.game.player_0.player_hearts != 0:
                self.game.draw_text('LEVEL ' + str(self.game.current_level), 30, self.level_x, self.level_y, self.game.mustard)
            else:
                self.game.draw_text('GAME OVER', 30, self.level_x, self.level_y, self.game.mustard)

            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.game.shoot is True:
            if self.game.game_reset is False:
                self.game.playing = True
                self.run_display = False
            else:
                self.game.player_0.set_player_hearts(3)
                self.game.game_reset = False
                self.game.current_menu = self.game.main_menu
                self.run_display = False


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.start_x, self.start_y = self.mid_w, self.mid_h - 60
        self.settings_x, self.settings_y = self.mid_w, self.mid_h - 10
        self.credits_x, self.credits_y = self.mid_w, self.mid_h + 40
        self.quit_x, self.quit_y = self.mid_w, self.mid_h + 90
        self.start_game_rect, self.settings_rect, self.credits_rect, self.quit_rect = 0, 0, 0, 0

        self.start_game_color = self.game.mustard
        self.settings_color = self.game.mustard
        self.credits_color = self.game.mustard
        self.quit_color = self.game.mustard

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            # self.game.menu_display.blit(self.vinewood_img, (self.mid_w - 270, 0))
            self.menu_animation()
            self.game.draw_text('Main Menu', 150, self.mid_w, 200, self.game.mustard, 'menu', 'title')
            self.start_game_rect = self.game.draw_text('START GAME', 40, self.start_x, self.start_y,
                                                       self.start_game_color)
            self.settings_rect = self.game.draw_text('SETTINGS', 40, self.settings_x, self.settings_y,
                                                     self.settings_color)
            self.credits_rect = self.game.draw_text('CREDITS', 40, self.credits_x, self.credits_y, self.credits_color)
            self.quit_rect = self.game.draw_text('QUIT GAME', 40, self.quit_x, self.quit_y, self.quit_color)
            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.start_game_rect.collidepoint((int(self.mx), self.my)):
            self.start_game_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.start_game_rect.x - 50, self.start_game_rect.y - 5))
            if self.game.click is True:
                self.game.current_level = 0
                self.game.current_menu = self.game.message_screen
                self.run_display = False
        else:
            self.start_game_color = self.game.mustard

        if self.settings_rect.collidepoint(self.mx, self.my):
            self.settings_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.settings_rect.x - 50, self.settings_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.options
                self.run_display = False
        else:
            self.settings_color = self.game.mustard

        if self.credits_rect.collidepoint(self.mx, self.my):
            self.credits_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.credits_rect.x - 50, self.credits_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.credits
                self.run_display = False
        else:
            self.credits_color = self.game.mustard

        if self.quit_rect.collidepoint(self.mx, self.my):
            self.game.menu_display.blit(self.cross_img, (self.quit_rect.x - 50, self.quit_rect.y - 5))
            self.quit_color = self.game.white
            if self.game.click is True:
                self.game.playing = False
                self.game.running = False
                self.run_display = False
        else:
            self.quit_color = self.game.mustard

        if self.game.back_key is True:
            self.game.playing = False
            self.game.running = False
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.vid_x, self.vid_y = self.mid_w, self.mid_h - 40
        self.vol_x, self.vol_y = self.mid_w, self.mid_h
        self.control_x, self.control_y = self.mid_w, self.mid_h + 40
        self.back_x, self.back_y = self.mid_w, self.mid_h + 80
        self.vid_rect, self.vol_rect, self.control_rect, self.back_rect = 0, 0, 0, 0

        self.vid_color = self.game.mustard
        self.vol_color = self.game.mustard
        self.control_color = self.game.mustard
        self.back_color = self.game.mustard

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            self.game.draw_text('Settings', 150, 400, 200, self.game.mustard, 'menu', 'title')
            self.vid_rect = self.game.draw_text('VIDEOS', 40, self.vid_x, self.vid_y, self.vid_color)
            self.vol_rect = self.game.draw_text('VOLUME', 40, self.vol_x, self.vol_y, self.vol_color)
            self.control_rect = self.game.draw_text('CONTROLS', 40, self.control_x, self.control_y, self.control_color)
            self.back_rect = self.game.draw_text('BACK', 40, self.back_x, self.back_y, self.back_color)

            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.vid_rect.collidepoint(self.mx, self.my):
            self.vid_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.vid_rect.x - 50, self.vid_rect.y - 5))
            if self.game.click is True:
                print("going to video settings")
        else:
            self.vid_color = self.game.mustard

        if self.vol_rect.collidepoint(self.mx, self.my):
            self.vol_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.vol_rect.x - 50, self.vol_rect.y - 5))
            if self.game.click is True:
                print("going to volume settings")
        else:
            self.vol_color = self.game.mustard

        if self.control_rect.collidepoint(self.mx, self.my):
            self.control_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.control_rect.x - 50, self.control_rect.y - 5))
            if self.game.click is True:
                print("going to controls settings")
        else:
            self.control_color = self.game.mustard

        if self.back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.back_rect.x - 50, self.back_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.main_menu
            self.run_display = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.back_x, self.back_y = self.mid_w, self.mid_h + 100
        self.back_rect = 0
        self.back_color = self.game.mustard

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            self.game.draw_text('CREATED BY:', 40, self.game.window_width / 2, self.game.window_height / 2 - 80,
                                self.game.mustard)
            self.game.draw_text('FILIP KOWALEWSKI', 80, self.game.window_width / 2, self.game.window_height / 2,
                                self.game.mustard, 'menu', 'title')

            self.back_rect = self.game.draw_text('BACK', 40, self.back_x, self.back_y, self.back_color)

            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.back_rect.x - 50, self.back_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.main_menu
            self.run_display = False


class PauseMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.resume_x, self.resume_y = self.mid_w, self.mid_h - 25
        self.menu_x, self.menu_y = self.mid_w, self.mid_h + 25
        self.resume_rect, self.menu_rect = 0, 0
        self.resume_color, self.menu_color = self.game.mustard, self.game.mustard

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            self.resume_rect = self.game.draw_text('RESUME GAME', 40, self.resume_x, self.resume_y, self.resume_color)
            self.menu_rect = self.game.draw_text('EXIT TO MENU', 40, self.menu_x, self.menu_y, self.menu_color)

            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.resume_rect.collidepoint(self.mx, self.my):
            self.resume_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (self.resume_rect.x - 50, self.resume_rect.y - 5))
            if self.game.click is True:
                self.game.playing = True
                self.run_display = False
        else:
            self.resume_color = self.game.mustard

        if self.menu_rect.collidepoint((self.mx, self.my)):
            self.game.menu_display.blit(self.cross_img, (self.menu_rect.x - 50, self.menu_rect.y - 5))
            self.menu_color = self.game.white
            if self.game.click is True:
                self.game.player_0.hearts_number = 0
                self.game.game_over()
                self.game.current_menu = self.game.main_menu
                self.run_display = False
        else:
            self.menu_color = self.game.mustard

        if self.game.back_key is True:
            self.game.playing = True
            self.run_display = False

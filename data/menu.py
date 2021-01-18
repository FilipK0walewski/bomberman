import pygame
import random
from data.bomb import Bomb
import json


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.window_width / 2
        self.mid_h = self.game.window_height / 2
        self.title_size = int(self.mid_w / 4)
        self.font_size = int(self.mid_w / 16)

        self.run_display = True
        self.run_animation = True
        self.temp_tick = 500
        self.y_spawn = - 32
        self.falling_bombs = []
        self.mx, self.my = 0, 0

        self.cross_img = pygame.image.load('data/assets/sprites/enemy/boss_miniature.png')
        self.cross_rect = self.cross_img.get_rect()

        self.font_color = self.game.mustard
        self.hover_font_color = self.game.white

        self.clock = pygame.time.Clock()

    def refresh_root(self):
        self.mid_w = self.game.window_width / 2
        self.mid_h = self.game.window_height / 2
        self.title_size = int(self.mid_w / 4)
        self.font_size = int(self.mid_w / 16)

    def screen_blit(self):
        self.game.window.blit(self.game.menu_display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def menu_animation(self):
        tick = pygame.time.get_ticks()
        delta_time = self.clock.tick(self.game.FPS) * .001 * self.game.go_to_fps
        if tick - self.temp_tick >= 500:
            self.temp_tick = pygame.time.get_ticks()
            x_spawn = random.randint(0, self.game.window_width + 32)
            falling_bomb_rect = pygame.Rect(x_spawn, self.y_spawn, 32, 32)
            bomb = Bomb(falling_bomb_rect, [], [], 1)
            self.falling_bombs.append(bomb)

        for bomb in self.falling_bombs:
            bomb.bomb_falling(self.game.menu_display, self.game.bomb_animation[0], delta_time)

            if bomb.bomb_rect.collidepoint(self.mx, self.my):
                if self.game.click:
                    # bomb.explosion()
                    self.falling_bombs.remove(bomb)

            if bomb.bomb_rect.y >= self.mid_h * 2 + 32:
                self.falling_bombs.remove(bomb)

########################################################################################################################


class GenerateMessage(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.spacing = self.mid_h * .03
        self.level_x, self.level_y = self.mid_w, self.mid_h * .9
        self.spacing = self.mid_h * .4
        self.border_0 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_0.center = (self.mid_w, 0)
        self.loading_rect = pygame.Rect(0, 0, 50, self.mid_h * .15)
        self.loading_rect.topleft = self.border_0.topleft

    def refresh(self):

        self.spacing = self.mid_h * .03
        self.level_x, self.level_y = self.mid_w, self.mid_h * .9
        self.border_0 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_0.center = (self.mid_w, 0)
        self.loading_rect = pygame.Rect(0, 0, 50, self.mid_h * .15)
        self.loading_rect.topleft = self.border_0.topleft

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            if self.game.player_0.current_health > 0:
                text_rect = self.game.draw_text('LOADING MAP', self.font_size, (self.mid_w, self.mid_h), self.game.mustard)
                self.border_0.top = text_rect.bottom + self.spacing
                self.loading_rect.top = text_rect.bottom + self.spacing
                pygame.draw.rect(self.game.menu_display, self.game.mustard, self.loading_rect, border_radius=5)
                pygame.draw.rect(self.game.menu_display, self.game.white, self.border_0, 5, border_radius=5)
                if self.loading_rect.width < self.border_0.width:
                    self.loading_rect.width += 10
                else:
                    self.game.draw_text('PRESS SPACE', int(self.font_size / 2), self.border_0.center, self.game.white)

            else:
                self.game.draw_text('GAME OVER', self.font_size, (self.level_x, self.level_y), self.game.mustard)

            self.check_input()
            self.screen_blit()

    def check_input(self):
        if self.game.shoot is True:
            if self.game.player_0.current_health > 0:
                if self.loading_rect.width == self.border_0.width:
                    self.game.playing = True
                    self.run_display = False
            else:
                self.game.game_over()
                self.game.current_menu = self.game.main_menu
                self.run_display = False

# MAIN MENU ############################################################################################################


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.start_y = self.mid_h * .85
        self.settings_y = self.mid_h
        self.credits_y = self.mid_h * 1.15
        self.quit_y = self.mid_h * 1.75
        self.name_pos = (self.mid_w, self.mid_h * .5)

        self.start_game_color = self.game.mustard
        self.settings_color = self.game.mustard
        self.credits_color = self.game.mustard
        self.quit_color = self.game.mustard

    def refresh(self):

        self.name_pos = (self.mid_w, self.mid_h * .5)
        self.start_y = self.mid_h * .85
        self.settings_y = self.mid_h
        self.credits_y = self.mid_h * 1.15
        self.quit_y = self.mid_h * 1.75

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()

            self.game.draw_text('Main Menu', self.title_size, self.name_pos, self.game.mustard, 'menu', 'center', False, 'title')
            start_game_rect = self.game.draw_text('START GAME', self.font_size, (self.mid_w, self.start_y),
                                                  self.start_game_color)
            settings_rect = self.game.draw_text('SETTINGS', self.font_size, (self.mid_w, self.settings_y),
                                                self.settings_color)
            credits_rect = self.game.draw_text('CREDITS', self.font_size, (self.mid_w, self.credits_y), self.credits_color)
            quit_rect = self.game.draw_text('QUIT GAME', self.font_size, (self.mid_w, self.quit_y), self.quit_color)

            self.check_input(start_game_rect, settings_rect, credits_rect, quit_rect)
            self.screen_blit()

    def check_input(self, start_game_rect, settings_rect, credits_rect, quit_rect):

        if start_game_rect.collidepoint((int(self.mx), int(self.my))):
            self.start_game_color = self.game.white
            self.cross_rect.topright = start_game_rect.topleft
            self.game.menu_display.blit(self.cross_img, self.cross_rect.topleft)
            if self.game.click is True:
                self.game.current_level = 0
                self.game.current_menu = self.game.message_screen
                self.run_display = False
        else:
            self.start_game_color = self.game.mustard

        if settings_rect.collidepoint((self.mx, self.my)):
            self.settings_color = self.game.white
            self.cross_rect.topright = settings_rect.topleft
            self.game.menu_display.blit(self.cross_img, self.cross_rect.topleft)
            if self.game.click is True:
                self.game.current_menu = self.game.options
                self.run_display = False
        else:
            self.settings_color = self.game.mustard

        if credits_rect.collidepoint(self.mx, self.my):
            self.credits_color = self.game.white
            self.cross_rect.topright = credits_rect.topleft
            self.game.menu_display.blit(self.cross_img, self.cross_rect.topleft)
            if self.game.click is True:
                self.game.current_menu = self.game.credits
                self.run_display = False
        else:
            self.credits_color = self.game.mustard

        if quit_rect.collidepoint(self.mx, self.my):
            self.cross_rect.topright = quit_rect.topleft
            self.game.menu_display.blit(self.cross_img, self.cross_rect.topleft)
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

# OPTIONS ##############################################################################################################


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.vid_x, self.vid_y = self.mid_w, self.mid_h * .85
        self.vol_x, self.vol_y = self.mid_w, self.mid_h
        self.control_x, self.control_y = self.mid_w, self.mid_h * 1.15
        self.back_x, self.back_y = self.mid_w, self.mid_h * 1.75

        self.name_pos = (self.mid_w, self.mid_h * .5)
        self.vid_color = self.game.mustard
        self.vol_color = self.game.mustard
        self.control_color = self.game.mustard
        self.back_color = self.game.mustard

    def refresh(self):

        self.name_pos = (self.mid_w, self.mid_h * .5)
        self.vid_x, self.vid_y = self.mid_w, self.mid_h * .85
        self.vol_x, self.vol_y = self.mid_w, self.mid_h
        self.control_x, self.control_y = self.mid_w, self.mid_h * 1.15
        self.back_x, self.back_y = self.mid_w, self.mid_h * 1.75

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:

            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            self.game.draw_text('Settings', self.title_size, (self.mid_w, self.mid_h * .5), self.game.mustard, 'menu', 'center', False, 'title')
            vid_rect = self.game.draw_text('VIDEOS', self.font_size, (self.vid_x, self.vid_y), self.vid_color)
            vol_rect = self.game.draw_text('VOLUME', self.font_size, (self.vol_x, self.vol_y), self.vol_color)
            control_rect = self.game.draw_text('CONTROLS', self.font_size, (self.control_x, self.control_y), self.control_color)
            back_rect = self.game.draw_text('BACK', self.font_size, (self.back_x, self.back_y), self.back_color)

            self.check_input(vid_rect, vol_rect, control_rect, back_rect)
            self.screen_blit()

    def check_input(self, vid_rect, vol_rect, control_rect, back_rect):
        if vid_rect.collidepoint(self.mx, self.my):
            self.vid_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (vid_rect.x - 50, vid_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.videos
                self.run_display = False
        else:
            self.vid_color = self.game.mustard

        if vol_rect.collidepoint(self.mx, self.my):
            self.vol_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (vol_rect.x - 50, vol_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.volume
                self.run_display = False
        else:
            self.vol_color = self.game.mustard

        if control_rect.collidepoint(self.mx, self.my):
            self.control_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (control_rect.x - 50, control_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.controls
                self.run_display = False
        else:
            self.control_color = self.game.mustard

        if back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (back_rect.x - 50, back_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.main_menu
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.main_menu
            self.run_display = False

# VIDEOS ###############################################################################################################


vec = pygame.math.Vector2


class VideosMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

        self.resolutions = [[800, 600], [1280, 720], [1600, 900], [1680, 1050], [1920, 1080]]
        self.full_screen = self.game.full_screen
        self.temp = 1
        self.fps = [26, 30, 60, 75, 120]
        self.fps_counter = 0
        self.rt = self.game.ray_tracing

        self.spacing = self.mid_h * .04

        self.resolution_y = self.mid_h * .25
        self.full_screen_y = self.mid_h * .6
        self.ray_tracing_y = self.mid_h * .95
        self.fps_y = self.mid_h * 1.3

        self.resolution_color, self.full_screen_color, self.full_screen_info_color = self.game.mustard, self.game.mustard, self.game.mustard
        self.resolution_info_color = self.game.mustard
        self.ray_color, self.fps_color = self.game.mustard, self.game.mustard

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75
        self.back_color, self.apply_color = self.game.mustard, self.game.mustard

    def refresh(self):

        self.refresh_root()
        self.resolution_y = self.mid_h * .25
        self.full_screen_y = self.mid_h * .6
        self.ray_tracing_y = self.mid_h * .95
        self.fps_y = self.mid_h * 1.3

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75
        self.spacing = self.mid_h * .04

    def display_menu(self):

        self.full_screen = self.game.full_screen
        self.rt = self.game.ray_tracing

        temp = 0
        for i in self.resolutions:
            if i[0] != self.game.window_width and i[1] != self.game.window_height:
                temp += 1
            else:
                break
        self.temp = temp

        self.fps_counter = 0
        for i in self.fps:
            if i != self.game.FPS:
                self.fps_counter += 1
            else:
                break

        self.run_display = True

        while self.run_display:

            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()

            resolution_rect = self.game.draw_text('RESOLUTION', self.font_size, (self.mid_w, self.resolution_y), self.resolution_color)

            resolution_info_rect = self.game.draw_text(str(self.resolutions[self.temp][0]) + 'x' + str(self.resolutions[self.temp][1]), self.font_size,
                                                       (self.mid_w, resolution_rect.bottom + self.spacing), self.resolution_info_color)

            full_screen_rect = self.game.draw_text('FULL SCREEN', self.font_size, (self.mid_w, self.full_screen_y), self.full_screen_color)

            full_screen_info_rect = self.game.draw_text(str(self.full_screen), self.font_size,  (self.mid_w, full_screen_rect.bottom + self.spacing),
                                                        self.full_screen_info_color)

            ray_tracing_rect = self.game.draw_text('RAY TRACING', self.font_size, (self.mid_w, self.ray_tracing_y), self.game.mustard)
            ray_tracing_info = self.game.draw_text(str(self.rt), self.font_size, (self.mid_w, ray_tracing_rect.bottom + self.spacing), self.ray_color)

            fps_rect = self.game.draw_text('FPS', self.font_size, (self.mid_w, self.fps_y), self.game.mustard)

            fps_info = self.game.draw_text(str(self.fps[self.fps_counter]), self.font_size, (self.mid_w, fps_rect.bottom + self.spacing), self.fps_color)

            apply_rect = self.game.draw_text('APPLY', self.font_size, (self.apply_x, self.apply_y), self.apply_color)
            back_rect = self.game.draw_text('BACK', self.font_size, (self.back_x, self.back_y), self.back_color)

            self.check_input(fps_info, ray_tracing_info, resolution_info_rect, full_screen_info_rect, apply_rect, back_rect)
            self.screen_blit()

    def check_input(self, fps, ray_tracing, resolution, full_screen, apply_rect, back_rect):

        if fps.collidepoint(self.mx, self.my):
            self.fps_color = self.game.white
            if self.game.click is True:
                self.fps_counter += 1
                if self.fps_counter == len(self.fps):
                    self.fps_counter = 0
        else:
            self.fps_color = self.game.mustard

        if ray_tracing.collidepoint(self.mx, self.my):
            self.ray_color = self.game.white
            if self.game.click is True:
                temp = self.rt
                if temp == 'on':
                    self.rt = 'off'
                else:
                    self.rt = 'on'
        else:
            self.ray_color = self.game.mustard

        if resolution.collidepoint(self.mx, self.my):
            self.resolution_info_color = self.game.white
            if self.game.click is True:
                self.temp += 1
                if self.temp >= len(self.resolutions):
                    self.temp = 0
        else:
            self.resolution_info_color = self.game.mustard

        if full_screen.collidepoint(self.mx, self.my):
            self.full_screen_info_color = self.game.white
            if self.game.click is True:
                temp = self.full_screen
                if temp == 'on':
                    self.full_screen = 'off'
                else:
                    self.full_screen = 'on'
        else:
            self.full_screen_info_color = self.game.mustard

        if back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (back_rect.x - 50, back_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.options
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if apply_rect.collidepoint(self.mx, self.my):
            self.apply_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (apply_rect.x - 50, apply_rect.y - 5))
            if self.game.click is True:
                resolution = (self.resolutions[self.temp])

                if self.full_screen == 'on':
                    self.game.window = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
                else:
                    self.game.window = pygame.display.set_mode(resolution, 0, 32)

                self.game.full_screen = self.full_screen

                self.game.menu_display = pygame.Surface(resolution)
                self.game.display = pygame.Surface((int(resolution[0] / 2), int(resolution[1] / 2)))
                self.game.window_width = resolution[0]
                self.game.window_height = resolution[1]

                self.game.ray_tracing = self.rt
                self.game.FPS = self.fps[self.fps_counter]

                self.game.json_data['screen']['resolution']['width'] = resolution[0]
                self.game.json_data['screen']['resolution']['height'] = resolution[1]
                self.game.json_data['screen']['fullscreen'] = self.full_screen
                self.game.json_data['screen']['ray_tracing'] = self.rt
                self.game.json_data['screen']['fps'] = self.fps[self.fps_counter]

                with open("startup.json", "w") as write_file:
                    json.dump(self.game.json_data, write_file)
                write_file.close()

                # player
                self.game.game_over(True)

                self.refresh()
        else:
            self.apply_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.options
            self.run_display = False


# SOUNDS ###############################################################################################################


class VolumeMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

        self.spacing = self.mid_h * .03

        self.max_music, self.max_sfx = 100, 100
        self.current_music, self.current_sfx = 100, 100

        self.music_y, self.effects_y = self.mid_h * .5, self.mid_h * 1.15

        self.rect_0 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_0 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.rect_0.center = (self.mid_w, 0)
        self.border_0.center = (self.mid_w, 0)

        self.rect_1 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_1 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.rect_1.center = (self.mid_w, 0)
        self.border_1.center = (self.mid_w, 0)

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75
        self.back_rect, self.apply_rect = 0, 0
        self.back_color, self.apply_color = self.game.mustard, self.game.mustard

    def refresh(self):

        self.spacing = self.mid_h * .03
        self.music_y, self.effects_y = self.mid_h * .5, self.mid_h * 1.15

        self.border_0 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_0.center = (self.mid_w, 0)
        percent = self.current_music / self.max_music
        self.rect_0.width = self.border_0.width * percent

        self.border_1 = pygame.Rect(0, 0, self.mid_w * .75, self.mid_h * .15)
        self.border_1.center = (self.mid_w, 0)
        percent = self.current_sfx / self.max_sfx
        self.rect_1.width = self.border_1.width * percent

        self.rect_0.topleft = self.border_0.topleft
        self.rect_0.height = self.border_0.height

        self.rect_1.topleft = self.border_1.topleft
        self.rect_1.height = self.border_1.height

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()

            music_rect = self.game.draw_text('MUSIC VOLUME', self.font_size, (self.mid_w, self.music_y), self.game.mustard)
            self.rect_0.top = music_rect.bottom + self.spacing
            pygame.draw.rect(self.game.menu_display, self.game.mustard, self.rect_0, border_radius=5)
            self.border_0.top = music_rect.bottom + self.spacing
            pygame.draw.rect(self.game.menu_display, self.game.white, self.border_0, 5, border_radius=5)
            music_percent = (self.current_music / self.max_music) * 100
            self.game.draw_text(str(round(music_percent)) + ' %', self.font_size, self.border_0.center, self.game.white)

            sfx_rect = self.game.draw_text('SOUND EFFECTS VOLUME', self.font_size, (self.mid_w, self.effects_y), self.game.mustard)
            self.rect_1.top = sfx_rect.bottom + self.spacing
            pygame.draw.rect(self.game.menu_display, self.game.mustard, self.rect_1, border_radius=5)
            self.border_1.top = sfx_rect.bottom + self.spacing
            pygame.draw.rect(self.game.menu_display, self.game.white, self.border_1, 5, border_radius=5)
            sfx_percent = (self.current_sfx / self.max_sfx) * 100
            self.game.draw_text(str(round(sfx_percent)) + ' %', self.font_size, self.border_1.center, self.game.white)

            apply_rect = self.game.draw_text('APPLY', self.font_size, (self.apply_x, self.apply_y), self.apply_color)
            back_rect = self.game.draw_text('BACK', self.font_size, (self.back_x, self.back_y), self.back_color)

            self.check_input(apply_rect, back_rect)
            self.screen_blit()

    def check_input(self, apply_rect, back_rect):

        if self.border_0.collidepoint(self.mx, self.my):
            if self.game.click is True:
                temp = self.mx - self.rect_0.left
                self.rect_0.width = temp
                self.current_music = self.rect_0.width / self.border_0.width * 100
                self.current_music = self.current_music

        if self.border_1.collidepoint(self.mx, self.my):
            if self.game.click is True:
                temp = self.mx - self.rect_1.left
                self.rect_1.width = temp
                self.current_sfx = self.rect_1.width / self.border_1.width * 100
                self.current_sfx = self.current_sfx

        if back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            if self.game.click is True:
                self.game.current_menu = self.game.options
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if apply_rect.collidepoint(self.mx, self.my):
            self.apply_color = self.game.white
            if self.game.click is True:
                pass
        else:
            self.apply_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.options
            self.run_display = False

# CONTROLS #############################################################################################################


class ControlsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)

        self.waiting = False

        self.move_right_x, self.move_right_y = self.mid_w * .1, self.mid_h * .1
        self.move_left_x, self.move_left_y = self.mid_w * .1, self.mid_h * .25
        self.move_up_x, self.move_up_y = self.mid_w * .1, self.mid_h * .4
        self.move_down_x, self.move_down_y = self.mid_w * .1, self.mid_h * .55

        self.bomb_x, self.bomb_y = self.mid_w * .1, self.mid_h * .7
        self.use_x, self.use_y = self.mid_w * .1, self.mid_h * .85
        self.enter_x, self.enter_y = self.mid_w * .1, self.mid_h
        self.space_x, self.space_y = self.mid_w * .1, self.mid_h * 1.15
        self.eq_x, self.eq_y = self.mid_w * .1, self.mid_h * 1.3
        self.a_x, self.a_y = self.mid_w * .1, self.mid_h * 1.45

        self.left_c, self.right_c, self.up_c, self.down_c = self.game.mustard, self.game.mustard, self.game.mustard, self.game.mustard
        self.bomb_c, self.use_c, self.enter_c, self.space_c, self.eq_c, self.a_c = self.game.mustard, self.game.mustard, self.game.mustard, self.game.mustard, self.game.mustard, self.game.mustard

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75
        self.back_color, self.apply_color = self.game.mustard, self.game.mustard

    def refresh(self):
        self.mid_w, self.mid_h = self.game.window_width / 2, self.game.window_height / 2

        self.move_right_x, self.move_right_y = self.mid_w * .1, self.mid_h * .1
        self.move_left_x, self.move_left_y = self.mid_w * .1, self.mid_h * .25
        self.move_up_x, self.move_up_y = self.mid_w * .1, self.mid_h * .4
        self.move_down_x, self.move_down_y = self.mid_w * .1, self.mid_h * .55

        self.bomb_x, self.bomb_y = self.mid_w * .1, self.mid_h * .7
        self.use_x, self.use_y = self.mid_w * .1, self.mid_h * .85
        self.enter_x, self.enter_y = self.mid_w * .1, self.mid_h
        self.space_x, self.space_y = self.mid_w * .1, self.mid_h * 1.15
        self.eq_x, self.eq_y = self.mid_w * .1, self.mid_h * 1.3
        self.a_x, self.a_y = self.mid_w * .1, self.mid_h * 1.45

        self.back_x, self.back_y = self.mid_w * .5, self.mid_h * 1.75
        self.apply_x, self.apply_y = self.mid_w * 1.5, self.mid_h * 1.75

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True

        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()

            self.game.draw_text('move right: ', self.font_size, (self.move_right_x, self.move_right_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('move left: ', self.font_size, (self.move_left_x, self.move_left_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('move up: ', self.font_size, (self.move_up_x, self.move_up_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('move down: ', self.font_size, (self.move_down_x, self.move_down_y), self.game.mustard, 'menu', 'topleft')

            self.game.draw_text('drop bomb: ', self.font_size, (self.bomb_x, self.bomb_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('enter door: ', self.font_size, (self.enter_x, self.enter_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('use: ', self.font_size, (self.use_x, self.use_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('weapon: ', self.font_size, (self.space_x, self.space_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('equipment: ', self.font_size, (self.eq_x, self.eq_y), self.game.mustard, 'menu', 'topleft')
            self.game.draw_text('take all: ', self.font_size, (self.a_x, self.a_y), self.game.mustard, 'menu', 'topleft')

            self.game.draw_text(self.game.right, self.font_size, (2 * self.mid_w - self.move_right_x, self.move_right_y), self.right_c, 'menu', 'topright', True)
            self.game.draw_text(self.game.left, self.font_size, (2 * self.mid_w - self.move_left_x, self.move_left_y), self.left_c, 'menu', 'topright', True)
            self.game.draw_text(self.game.up, self.font_size, (2 * self.mid_w - self.move_up_x, self.move_up_y), self.up_c, 'menu', 'topright', True)
            self.game.draw_text(self.game.down, self.font_size, (2 * self.mid_w - self.move_down_x, self.move_down_y), self.down_c, 'menu', 'topright', True)

            self.game.draw_text(self.game.q, self.font_size, (2 * self.mid_w - self.bomb_x, self.bomb_y), self.bomb_c, 'menu', 'topright', True)
            self.game.draw_text(self.game.enter, self.font_size, (2 * self.mid_w - self.enter_x, self.enter_y), self.game.mustard, 'menu', 'topright', True)
            self.game.draw_text(self.game.use, self.font_size, (2 * self.mid_w - self.use_x, self.use_y), self.game.mustard, 'menu', 'topright', True)

            self.game.draw_text(self.game.weapon, self.font_size, (2 * self.mid_w - self.space_x, self.space_y), self.game.mustard, 'menu', 'topright', True)

            self.game.draw_text(self.game.tab, self.font_size, (2 * self.mid_w - self.eq_x, self.eq_y), self.game.mustard, 'menu', 'topright', True)
            self.game.draw_text(self.game.take_all, self.font_size, (2 * self.mid_w - self.a_x, self.a_y), self.game.mustard, 'menu', 'topright', True)

            apply_rect = self.game.draw_text('APPLY', self.font_size, (self.apply_x, self.apply_y), self.apply_color)
            back_rect = self.game.draw_text('BACK', self.font_size, (self.back_x, self.back_y), self.back_color)

            self.check_input(back_rect, apply_rect)
            self.screen_blit()

    def check_input(self, back_rect, apply_rect):

        if back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (back_rect.x - 50, back_rect.y - 5))
            if self.game.click is True:
                self.game.current_menu = self.game.options
                self.run_display = False
        else:
            self.back_color = self.game.mustard

        if apply_rect.collidepoint(self.mx, self.my):
            self.apply_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (apply_rect.x - 50, apply_rect.y - 5))
            if self.game.click is True:
                pass
        else:
            self.apply_color = self.game.mustard

        if self.game.back_key is True:
            self.game.current_menu = self.game.options
            self.run_display = False

    def read_key(self):
        pygame.draw.circle(self.game.menu_display, self.game.mustard, (self.mid_w, self.mid_h), self.mid_h * .6)
        self.game.draw_text('press the button', 40, (self.mid_w, self.mid_h), self.game.black)

# CREDITS ##############################################################################################################


class CreditsMenu(Menu):

    def __init__(self, game):
        Menu.__init__(self, game)
        self.back_x, self.back_y = self.mid_w, self.mid_h * 1.75
        self.created_by_y = self.mid_h * .5
        self.back_color = self.game.mustard

    def refresh(self):

        self.mid_w, self.mid_h = self.game.window_width / 2, self.game.window_height / 2
        self.back_x, self.back_y = self.mid_w, self.mid_h * 1.75
        self.created_by_y = self.mid_h * .5

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            self.game.draw_text('CREATED BY:', self.font_size, (self.mid_w, self.created_by_y), self.game.mustard)
            self.game.draw_text('Filip Kowalewski', self.title_size, (self.mid_w, self.mid_h),
                                self.game.mustard, 'menu', 'center', False, 'title')

            back_rect = self.game.draw_text('BACK', self.font_size, (self.back_x, self.back_y), self.back_color)

            self.check_input(back_rect)
            self.screen_blit()

    def check_input(self, back_rect):
        if back_rect.collidepoint(self.mx, self.my):
            self.back_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (back_rect.x - 50, back_rect.y - 5))
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

        self.resume_x, self.resume_y = self.mid_w, self.mid_h * .8
        self.menu_x, self.menu_y = self.mid_w, self.mid_h * 1.2
        self.resume_color, self.menu_color = self.game.mustard, self.game.mustard

    def refresh(self):

        self.resume_x, self.resume_y = self.mid_w, self.mid_h * .8
        self.menu_x, self.menu_y = self.mid_w, self.mid_h * 1.2

    def display_menu(self):

        self.refresh_root()
        self.refresh()
        self.run_display = True
        while self.run_display:
            self.mx, self.my = pygame.mouse.get_pos()
            self.game.check_events()
            self.game.menu_display.fill(self.game.black)
            self.menu_animation()
            resume_rect = self.game.draw_text('RESUME GAME', self.font_size, (self.resume_x, self.resume_y), self.resume_color)
            menu_rect = self.game.draw_text('EXIT TO MENU', self.font_size, (self.menu_x, self.menu_y), self.menu_color)

            self.check_input(resume_rect, menu_rect)
            self.screen_blit()

    def check_input(self, resume_rect, menu_rect):
        if resume_rect.collidepoint(self.mx, self.my):
            self.resume_color = self.game.white
            self.game.menu_display.blit(self.cross_img, (resume_rect.x - 50, resume_rect.y - 5))
            if self.game.click is True:
                self.game.playing = True
                self.run_display = False
        else:
            self.resume_color = self.game.mustard

        if menu_rect.collidepoint((self.mx, self.my)):
            self.game.menu_display.blit(self.cross_img, (menu_rect.x - 50, menu_rect.y - 5))
            self.menu_color = self.game.white
            if self.game.click is True:
                self.game.game_over()
                self.game.current_menu = self.game.main_menu
                self.run_display = False
        else:
            self.menu_color = self.game.mustard

        if self.game.back_key is True:
            self.game.playing = True
            self.run_display = False

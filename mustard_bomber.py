import pygame
import sys
from pygame import *
from bomberman.player import Player
from bomberman.map import Map
from bomberman.bomb import Bomb
from bomberman.enemy import Enemy

clock = pygame.time.Clock()
pygame.init()

pygame.display.set_caption("The Game")
window_width = 800
window_height = 600

windowSize = (window_width, window_height)

surface = pygame.display.set_mode(windowSize, 0, 32)
display = pygame.Surface((int(window_width), int(window_height)))

bombDropped = False
bombExploded = False
bombPause = False
explosion_length = 1

door_spawned = False
running = True

bombs = []
bombTicks = []
enemies = []
levels = []
bomb_rect = []
x = 0

font = pygame.font.SysFont(None, 20)
click = False

for n in range(2):
    level = Map(display, n)
    levels.append(level)

spawn = levels[x].get_spawn_rect()
player_0 = Player(window_width, window_height, display, spawn)


def reset():
    global door_spawned, enemies, bombs, spawn
    enemies = []
    player_0.set_player_hp(100)
    player_0.find_spawn_position(spawn)

    spawn = levels[x].get_spawn_rect()

    for m in range((x + 1) * 3):
        enemy = Enemy(spawn, display)
        enemy.load_image()
        enemies.append(enemy)

    door_spawned = False


def update_game():
    global bombDropped, bombPause, door_spawned, running, x, explosion_length

    r = levels[x].get_tile_rect()

    player_0.move_player(r,  bomb_rect)
    player_rect = player_0.get_player_rect()

    if bombDropped is True:
        current_tick = pygame.time.get_ticks()
        bombTicks.append(current_tick)

        bomb = Bomb(player_0.get_player_rect(), display, levels[x].get_hard_wall(), explosion_length)
        bomb_rect.append(bomb.get_bomb_rect())
        bombs.append(bomb)
        bomb.move_bomb(levels[0].get_tile_rect())
        bombPause = True
        bombDropped = False

    if bombPause is True and pygame.time.get_ticks() - bombTicks[-1] > 500:
        bombPause = False

    for t in bombTicks:
        if pygame.time.get_ticks() - t > 3000:
            er = bombs[0].get_explosion_rect()
            levels[x].wall_destroying(er)

            for tile in er:
                if tile.colliderect(player_0.get_player_rect()):
                    player_0.set_player_hp(-100)
                for alien in enemies:
                    if tile.colliderect(alien.get_rect()):
                        alien.take_damage(200)

            if pygame.time.get_ticks() - t > 4000:
                bombs.pop(0)
                player_0.add_bomb()
                bomb_rect.pop(0)
                bombTicks.pop(0)

    # enemy-player collision
    for alien in enemies:
        alien.move_enemy(r, bomb_rect)
        alien_rect = alien.get_rect()
        if alien_rect.colliderect(player_0.get_player_rect()):
            player_0.set_player_hp(-100)
            reset()
        if alien.get_hp() <= 0:
            enemies.remove(alien)

    if len(enemies) == 0 and levels[x].check_door() is False:
        levels[x].open_the_door()
        print("player: ", player_rect.x, " ", player_rect.y)
        print("all dead")

    if levels[x].check_door() is True:
        if levels[x].get_door_rect().colliderect(player_0.get_player_rect()):
            pygame.mouse.set_visible(True)
            x += 1
            if x == 2:
                x = 0
            reset()

    # coins
    bomb_coins_rect = levels[x].get_bomb_coin_rect()
    explosion_coins_rect = levels[x].get_explosion_coin_rect()

    for rect in bomb_coins_rect:
        if player_rect.colliderect(rect):
            player_0.add_bomb()
            levels[x].coin_picking(rect, 'bomb')

    for rect in explosion_coins_rect:
        if player_rect.colliderect(rect):
            explosion_length += 1
            levels[x].coin_picking(rect, 'explosion')


def draw_game():
    display.fill((255, 192, 203))
    s = player_0.scroll()

    levels[x].tile_map_reset()
    levels[x].display_map(s)

    for bomb in bombs:
        bomb.draw_bomb(s)
        bomb.explosion()
        bomb.draw_explosion(s)

    for alien in enemies:
        alien.draw_enemy(s)

    player_0.draw_player(s)


def quit_game():
    pygame.quit()
    sys.exit()


def draw_text(text, font_, color_, sur, x, y):
    text_obj = font_.render(text, 1, color_)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (int(x), int(y))
    sur.blit(text_obj, text_rect)


def game():
    reset()
    pygame.mouse.set_visible(False)
    global running, bombDropped
    running = True
    while running:

        update_game()
        draw_game()

        for game_event in pygame.event.get():
            if game_event.type == QUIT:
                quit_game()
            if game_event.type == KEYDOWN:
                if game_event.key == K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    running = False
                if game_event.key == K_SPACE:
                    if bombPause is False and player_0.get_bomb_number() != 0:
                        bombDropped = True
                if game_event.type == KEYDOWN:
                    if game_event.key == K_SPACE:
                        if player_0.get_bomb_number() != 0:
                            player_0.remove_bomb()

        surface.blit(pygame.transform.scale(display, windowSize), (0, 0))
        pygame.display.update()
        clock.tick(60)


def main_menu():

    global click
    while True:
        surface.fill((255, 192, 203))
        draw_text('main menu', font, (255, 255, 255), surface, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(int(window_width / 2 - 100), 100, 200, 50)
        button_2 = pygame.Rect(int(window_width / 2 - 100), 200, 200, 50)
        if button_1.collidepoint(mx, my):
            if click:
                game()
                pygame.mouse.set_visible(True)
        if button_2.collidepoint(mx, my):
            if click:
                options()
        pygame.draw.rect(surface, (255, 0, 0), button_1)
        pygame.draw.rect(surface, (255, 0, 0), button_2)

        click = False
        for e in pygame.event.get():
            if e.type == QUIT:
                quit_game()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    quit_game()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


def options():
    pygame.mouse.set_visible(True)
    running_options = True
    while running_options:
        surface.fill((255, 192, 203))
        draw_text('options', font, (255, 255, 255), surface, window_width / 2 - 25, 20)

        for e in pygame.event.get():
            if e.type == QUIT:
                quit_game()
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running_options = False

        pygame.display.update()
        clock.tick(60)


# START
main_menu()

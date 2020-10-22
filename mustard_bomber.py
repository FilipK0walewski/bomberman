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

door_spawned = False
running = True

bombs = []
bombTicks = []
enemies = []
levels = []
bomb_rect = []
x = 0

player_0 = Player
enemy_0 = Enemy
level = Map
bomb_0 = Bomb

font = pygame.font.SysFont(None, 20)
click = False

for n in range(2):
    level = Map(display)
    levels.append(level)


def reset():
    global door_spawned, player_0

    levels[x].load_map('assets/maps/map_' + str(x) + '.txt')
    levels[x].load_images()

    spawn = levels[x].get_spawn_rect()

    for m in range((x + 1) * 3):
        enemy = Enemy(spawn, display)
        enemy.load_image()
        enemies.append(enemy)

    spawn = levels[x].get_spawn_rect()

    player_0 = Player(window_width, window_height, display, spawn)
    player_0.load_images()

    door_spawned = False
    levels[x].remove_door()


def update_game():
    global bombDropped, bombPause, door_spawned, running, x, player_0

    if bombDropped is True:
        current_tick = pygame.time.get_ticks()
        bombTicks.append(current_tick)

        player_rect = player_0.get_player_rect()

        bomb = Bomb(player_rect, display)
        bomb_rect.append(bomb.get_bomb_rect())
        bomb.load_images()
        bombs.append(bomb)
        bomb.move_bomb(levels[0].get_tile_rect())
        bombPause = True
        bombDropped = False

    if bombPause is True and pygame.time.get_ticks() - bombTicks[-1] > 1000:
        bombPause = False

    r = levels[x].get_tile_rect()

    player_0.move_player(r)
    player_rect = player_0.get_player_rect()

    for t in bombTicks:
        if pygame.time.get_ticks() - t > 3000:
            bombs[0].explosion()
            er = bombs[0].get_explosion_rect()
            levels[x].wall_destroying(er)

            for tile in er:
                if tile.colliderect(player_0.get_player_rect()):
                    player_0.set_player_hp(-20)
                for alien in enemies:
                    if tile.colliderect(alien.get_rect()):
                        alien.take_damage(20)

            bombs.pop(0)
            bomb_rect.pop(0)
            bombTicks.pop(0)

    for alien in enemies:
        alien.move_enemy(r, bomb_rect)
        if alien.get_hp() <= 0:
            enemies.remove(alien)

    if len(enemies) == 0 and door_spawned is False:
        levels[x].spawn_door()
        print("player: ", player_rect.x, " ", player_rect.y)
        print("all dead")
        door_spawned = True

    if levels[x].check_door() is True:
        if levels[x].get_door_rect().colliderect(player_0.get_player_rect()):
            pygame.mouse.set_visible(True)
            x += 1
            if x == 2:
                x = 0
            reset()


def draw_game():
    display.fill((255, 192, 203))
    s = player_0.scroll()

    levels[x].tile_map_reset()
    levels[x].display_map(s)

    for bomb in bombs:
        bomb.draw_bomb(s)

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

        if int(player_0.get_player_hp()) <= 0:
            running = False

        for event in pygame.event.get():
            if event.type == QUIT:
                quit_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.mouse.set_visible(True)
                    running = False
                if event.key == K_SPACE:
                    if bombPause is False:
                        bombDropped = True

        surface.blit(pygame.transform.scale(display, windowSize), (0, 0))
        pygame.display.update()
        clock.tick(60)


def main_menu():
    pygame.mouse.set_visible(True)
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

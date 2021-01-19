from data.game import Game
import pygame

g = Game()
pygame.mixer.music.load('data/assets/sounds/background_music.mp3')
pygame.mixer.music.play()
while g.running:
    g.current_menu.display_menu()
    g.game_loop()

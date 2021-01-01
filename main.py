from data.game import Game

g = Game()
# pygame.mixer.music.load('assets/sounds/8bit.mp3')
while g.get_running():
    # pygame.mixer.music.play()
    g.current_menu.display_menu()
    g.game_loop()

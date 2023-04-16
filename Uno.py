import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import GamePage
from Setting import Setting
from Game import Game
from Player import Player, Computer
from Map import MapPage

if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("Uno Game")

    game = Game([Player("PLAYER0"), Computer("computer0")], setting.color_weak)

    main_page = MainPage(screen)
    setting_page = SettingPage(screen, setting)
    game_page = GamePage(screen, setting, game)
    map_page = MapPage(screen, setting)

    page = main_page.running()
    while True:
        if page == "main":
            page = main_page.running()
        if page == "setting":
            page = setting_page.running()
        if page == "game":
            page = game_page.running()
        if page == "map":
            page = map_page.running()
        if page == "exit":
            exit(0)

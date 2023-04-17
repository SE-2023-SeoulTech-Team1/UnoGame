import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import GamePage
from Setting import Setting
from Game import Game
from Player import Player, Computer
from Map import MapPage
from PausedPage import PausedPage

if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("Uno Game")


    main_page = MainPage(screen)
    setting_page = SettingPage(screen, setting)
    game_page = GamePage(screen, setting)
    map_page = MapPage(screen, setting)
    pause_page = PausedPage(screen)

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
        if page == "pause":
            page = pause_page.running()
        

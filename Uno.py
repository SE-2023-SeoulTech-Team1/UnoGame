import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import GamePage
from Setting import Setting
from Game import Game
from Player import Player, Computer
from MapPage import MapPage
from PausedPage import PausedPage


if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("Uno Game")
    save_game_state = None
    main_page = MainPage(screen)
    setting_page = SettingPage(screen, setting)
    map_page = MapPage(screen, setting)
    pause_page = PausedPage(screen, setting, save_game_state)

    page = main_page.running()

    while True:
        if page == "main":
            page = main_page.running()
        elif page == "setting":
            page = setting_page.running()
        elif page == "game":
            game_page = GamePage(screen, setting)
            if save_game_state:
                game_page.game = save_game_state
            page = game_page.running()

        elif page == "game_level0":
            game_page_level0 = GamePage(screen, setting)
            page = game_page_level0.running()
        elif page == "game_level1":
            game_page_level1 = GamePage(screen, setting)
            page = game_page_level1.running()
        elif page == "game_level2":
            game_page_level2 = GamePage(screen, setting)
            page = game_page_level2.running()
        elif page == "game_level3":
            game_page_level3 = GamePage(screen, setting)
            page = game_page_level3.running()

        elif page == "map":
            page = map_page.running()
        elif page == "pause":
            state, page = pause_page.running()
        elif page == "exit":
            exit(0)

        

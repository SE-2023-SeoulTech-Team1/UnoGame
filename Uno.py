import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import GamePage
from Setting import Setting
from Game import Game
from Player import Player, Computer
from MapPage import MapPage
from PausedPage import PausedPage
import pickle
import os
import atexit



if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    if os.path.exists('setting_state.pkl'):
            with open('setting_state.pkl', 'rb') as f:
                setting_state = pickle.load(f)
            setting = setting_state
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("Uno Game")

    main_page = MainPage(screen)
    setting_page = SettingPage(screen, setting)
    map_page = MapPage(screen, setting)
    pause_page = PausedPage(screen, setting)

    page = main_page.running()
    def delete_pickle():
        if os.path.exists('game_state.pkl'):
            os.remove('game_state.pkl')


    while True:
        if page == "main":
            page = main_page.running()
        elif page == "setting":
            page = setting_page.running()
        elif page == "game":
            game_page = GamePage(screen, setting)
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
            page = pause_page.running()
        elif page == "exit":
            atexit.register(delete_pickle)
            exit(0)


        

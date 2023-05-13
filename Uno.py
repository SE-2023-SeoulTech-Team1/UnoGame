import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import GamePage
from LobbyPage import LobbyPage
from AchievementPage import AchievementPage
from Setting import Setting
from MapPage import MapPage
# from StoryLobbyPage import StoryLobbyPage
from PausedPage import PausedPage
import pickle
import os
import atexit


def delete_pickle():
    if os.path.exists('game_state.pkl'):
        os.remove('game_state.pkl')

def load_achievements():
    with open('achievements.pkl', 'rb') as f:
        achievements = pickle.load(f)

def save_achievements(achievements):
    with open('achievements.pkl', 'wb') as f:
        pickle.dump(achievements, f, pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    if os.path.exists('../setting_state.pkl'):
            with open('../setting_state.pkl', 'rb') as f:
                setting_state = pickle.load(f)
            setting = setting_state
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("Uno Game")
    main_page = MainPage(screen)
    setting_page = SettingPage(screen, setting)
    map_page = MapPage(screen, setting)
    pause_page = PausedPage(screen, setting)
    achievement_page = AchievementPage(screen, setting)

    page = main_page.running()
    while True:
        if len(page) == 2:
            # 이전 페이지가 게임 페이지 일 때 
            if page[1] == "game":
                setting_page = SettingPage(screen, setting, page[1])
                page = setting_page.running()
            elif page[1] == "main":
                setting_page = SettingPage(screen, setting, page[1])
                page = setting_page.running()
            else: 
                game_page = GamePage(screen, setting, page[1])
                page = game_page.running()
        if page == "main":
            page = main_page.running()
        elif page == "setting":
            page = setting_page.running()
        elif page == "lobby":
            lobby_page = LobbyPage(screen, setting)
            page = lobby_page.running()
        elif page == "game":
            game_page = GamePage(screen, setting)
            page = game_page.running()
        elif page == "game_level0":
            game_page_level0 = GamePage(screen, setting, ["Player", "Alien"], achievement_page.achievements)
            page = game_page_level0.running()
        elif page == "game_level1":
            game_page_level1 = GamePage(screen, setting, ["Player", "Alien0", "Alien1", "Alien2"], achievement_page.achievements)
            page = game_page_level1.running()
        elif page == "game_level2":
            game_page_level2 = GamePage(screen, setting, ["Player", "Alien0", "Alien1"], achievement_page.achievements)
            page = game_page_level2.running()
        elif page == "game_level3":
            game_page_level3 = GamePage(screen, setting)
            page = game_page_level3.running()
        elif page == "map":
            page = map_page.running()
        # elif page == "story_lobby":
        #     story_lobby_page = StoryLobbyPage(screen, setting)
        #     page = story_lobby_page.running()
        elif page == "achievement":
            page = achievement_page.running()
        elif page == "pause":
            page = pause_page.running()
        elif page == "exit":
            atexit.register(delete_pickle)
            save_achievements(achievement_page.achievements)
            exit(0)




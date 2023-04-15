import pygame
from MainPage import MainPage
from SettingPage import SettingPage
from GamePage import startGamePage

if __name__ == "__main__":
    pygame.init()

    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Uno Game")

    main_page = MainPage(screen)
    setting_page = SettingPage(screen)

    page = main_page.running()
    while True:
        if page == "main":
            page = main_page.running()
        if page == "setting":
            page = setting_page.running()
        if page == "game":
            page = startGamePage()
        if page == "exit":
            exit(0)

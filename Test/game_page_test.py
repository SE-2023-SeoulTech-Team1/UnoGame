import pygame
from GamePage import *
from Setting import *

if __name__ == "__main__":
    pygame.init()

    setting = Setting()
    screen = pygame.display.set_mode(setting.screen_size)
    pygame.display.set_caption("GamePage Test")
    game_page = GamePage(screen, setting, ["Player1", "Player2", "Player3", "Player4", "Player5"])

    game_page.running()
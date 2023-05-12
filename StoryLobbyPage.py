import pygame
import pygame_gui
from Colors import *

class StoryLobbyPage:
    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
    
    def running(self):
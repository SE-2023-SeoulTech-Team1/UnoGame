import pygame
from Colors import *

class Text():
    def __init__(self, x, y, text="Text", color=BLACK, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        FONT = pygame.font.SysFont('arialroundedmtbold', self.size)
        self.font = FONT.render(self.text, True, self.color, None)
        self.text_rect = self.font.get_rect()

    def render(self, screen):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.text_rect.center = (screen_width * self.x, screen_height * self.y)
        screen.blit(self.font, self.text_rect)
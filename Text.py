import pygame
from Colors import *

class Text():
    def __init__(self, x, y, text="Text", color=BLACK, size=24):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.size = size
        self.font = pygame.font.SysFont('arialrounded', size).render(self.text, True, self.color, None)

    def render(self, screen):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.top = screen_width * self.x
        self.left = screen_height * self.y
        self.rect = pygame.Rect(self.top, self.left, 100, 100)
        screen.blit(self.font, self.rect)

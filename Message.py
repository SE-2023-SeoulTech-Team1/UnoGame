import time
import pygame
from Colors import *

class Message():
    def __init__(self, screen, text, size, color):
        self.screen = screen
        self.text = text
        self.size = size
        self.color = color

    def draw(self):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        text = FONT.render(self.text, True, self.color, None)
        text_rec = text.get_rect()
        text_rec.top = 100
        text_rec.left = screen_width // 3
        self.screen.blit(text, text_rec)
        pygame.display.update()
        time.sleep(1)
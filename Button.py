import pygame
import sys
from Colors import *


class Button():
    def __init__(self, x,  y, width, height, text = 'Button', background_color=RED, hover_color=RED_HOVER, text_color=BLACK, text_size = 24):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = (screen_width * self.x) - (self.width / 2)
        self.left = (screen_height * self.y) - (self.height / 2)
        self.key_hovered = False
        self.colors = {
            'normal': background_color,
            'hover': hover_color,
        }
        self.background_color = background_color
        self.text_color = text_color
        self.text_size = text_size
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.top, self.left, self.width, self.height)
        font = pygame.font.SysFont('arialroundedmtbold', self.text_size)
        self.text = text


    def process(self, screen, hover=False):

        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.top = (screen_width * self.x) - (self.width / 2)
        self.left = (screen_height * self.y) - (self.height / 2)
        self.rect = pygame.Rect(self.top, self.left, self.width, self.height)

        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.surface.fill(self.colors['hover'])
        elif self.key_hovered:
            self.surface.fill(self.colors['hover'])
        else:
            self.surface.fill(self.colors['normal'])

        text_render = font.render(self.text, True, self.text_color)
        self.surface.blit(text_render, [
            self.rect.width/2 - text_render.get_rect().width/2,
            self.rect.height/2 - text_render.get_rect().height/2
        ])

        screen.blit(self.surface, self.rect)


class Text(Button):
    def __init__(self, x, y, width, height, text = 'Button', background_color=WHITE, hover_color=LIGHT_GRAY, text_color=BLACK, text_size = 24):
        super().__init__(x, y, width, height, text = text, background_color=background_color, hover_color=hover_color, text_color=text_color, text_size = text_size)
        self.colors = {
            'normal': '#FFFFFF',
            'hover': '#EEEEEE',
        }
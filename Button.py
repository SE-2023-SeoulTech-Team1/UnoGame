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

        text_render = FONT.render(self.text, True, self.text_color)
        self.surface.blit(text_render, [
            self.rect.width/2 - text_render.get_rect().width/2,
            self.rect.height/2 - text_render.get_rect().height/2
        ])

        screen.blit(self.surface, self.rect)


class TextButton(Button):
    def __init__(self, x, y, width, height, text = 'Button', background_color=WHITE, hover_color=LIGHT_GRAY, text_color=BLACK, text_size = 24):
        super().__init__(x, y, width, height, text = text, background_color=background_color, hover_color=hover_color, text_color=text_color, text_size = text_size)
        self.colors = {
            'normal': '#FFFFFF',
            'hover': '#EEEEEE',
        }

class Slider():
    def __init__(self, x, y, width, height, text_color=BLACK, text_size = 24):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.text_size = text_size
        self.font = pygame.font.SysFont('arialroundedmtbold', self.text_size)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.length = 200
        self.top = (screen_width * self.x) - (self.width / 2)
        self.left = (screen_height * self.y) - (self.height / 2) + 25
        self.rect = pygame.Rect(self.top, self.left - 5, self.length, 10)
        self.surface = pygame.Surface((self.width, self.height))
        self.min_val = 0
        self.max_val = 100
        self.value = 50

    def process_slider(self, screen):
        pygame.draw.rect(screen, GRAY, [self.top, self.left - 5, self.length, 10])
        pygame.draw.rect(screen, BLACK, [self.top + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.length) - 5, self.left - 10, 10, 20])

        text_min = self.font.render(str(self.min_val), True, GRAY)
        screen.blit(text_min, [self.top - text_min.get_width() / 2, self.left + 15])
        text_max = self.font.render(str(self.max_val), True, GRAY)
        screen.blit(text_max, [self.top + self.length - text_max.get_width() / 2, self.left + 15])
        text_value = self.font.render(str(self.value), True, BLACK)
        screen.blit(text_value, [self.top + int((self.value - self.min_val) / (self.max_val - self.min_val) * self.length) - text_value.get_width() / 2, self.left - 25])

import pygame
import pygame_gui
from Game import Game
from Player import Player, Computer
from Button import *
from Colors import *
from Text import *

class MapPage:
    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.img = pygame.transform.scale(pygame.image.load("./assets/map.png"), (self.screen_width, self.screen_height))
        self.level0_txt = Text(0.05, 0.65, "LEVEL 0", WHITE)
        self.level1_txt = Text(0.35, 0.35, "LEVEL 1", WHITE)
        self.level2_txt = Text(0.6, 0.65, "LEVEL 2", WHITE)
        self.level3_txt = Text(0.8, 0.35, "LEVEL 3", WHITE)


    def running(self):
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.img = pygame.transform.scale(pygame.image.load("./assets/map.png"), (self.screen_width, self.screen_height))

        self.screen.blit(self.img, (0, 0))
        self.level0_txt.render(self.screen)
        self.level1_txt.render(self.screen)
        self.level2_txt.render(self.screen)
        self.level3_txt.render(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.level0_txt.rect.collidepoint(event.pos):
                    return "game_level0"
                elif self.level1_txt.rect.collidepoint(event.pos):
                    return "game_level1"
                elif self.level2_txt.rect.collidepoint(event.pos):
                    return "game_level2"
                elif self.level3_txt.rect.collidepoint(event.pos):
                    return "game_level3"

        pygame.display.update()
        return "map"
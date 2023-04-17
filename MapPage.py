import pygame
import pygame_gui
from Game import Game
from Player import Player, Computer
from Button import *
from Colors import *

class MapPage:
    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.img = pygame.transform.scale(pygame.image.load("./assets/map.png"), (self.screen_width, self.screen_height))
        self.A_txt = font.render("A", True, WHITE, None)
        self.A_txt_box = pygame.Rect((self.screen_width * 0.09, self.screen_height * 0.65), (100, 100))

        game0 = Game([Player("PLAYER0"), Computer("COMPUTER0")])
        game1 = Game([Player("PLAYER1"), Computer("COMPUTER1")])
        game2 = Game([Player("PLAYER2"), Computer("COMPUTER2")])
        game3 = Game([Player("PLAYER3"), Computer("COMPUTER3")])


    def running(self):
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.img = pygame.transform.scale(pygame.image.load("./assets/map.png"), (self.screen_width, self.screen_height))
        self.A_txt_box = pygame.Rect((self.screen_width * 0.09, self.screen_height * 0.65), (100, 100))

        self.screen.blit(self.img, (0, 0))
        self.screen.blit(self.A_txt, self.A_txt_box)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.A_txt_box.collidepoint(event.pos):
                    return "game"

        pygame.display.update()
        return "map"
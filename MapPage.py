import pygame
import pygame_gui
from Game import Game
from Player import Player, Computer
from Button import *
from Colors import *
from Text import *
from resource_path import *
from PausedPage import PausedPage

class MapPage:
    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.font = pygame.font.SysFont('arialroundedmtblod', 22)
        self.img = pygame.transform.scale(pygame.image.load(resource_path("./assets/map.jpg")), (self.screen_width, self.screen_height))
        self.level0_txt = Text(0.05, 0.75, "LEVEL 0", WHITE)
        self.level1_txt = Text(0.35, 0.45, "LEVEL 1", WHITE)
        self.level2_txt = Text(0.6, 0.75, "LEVEL 2", WHITE)
        self.level3_txt = Text(0.8, 0.45, "LEVEL 3", WHITE)
        self.level0_img = pygame.image.load(resource_path("./assets/planet0.png"))
        self.level1_img = pygame.image.load(resource_path("./assets/planet1.png"))
        self.level2_img = pygame.image.load(resource_path("./assets/planet2.png"))
        self.level3_img = pygame.image.load(resource_path("./assets/planet3.png"))
        self.level_imgs = [self.level0_img, self.level1_img, self.level2_img, self.level3_img]
        self.level0_rect = self.level0_img.get_rect()
        self.level1_rect = self.level1_img.get_rect()
        self.level2_rect = self.level2_img.get_rect()
        self.level3_rect = self.level3_img.get_rect()
        self.game_start = False

        self.paused = False
        self.pause_page = PausedPage(self.screen, self.setting)


    def about_stage(self, screen, x, y):
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.level0_about = ["  < GAME RULE >", "  Computer 50% more skill card", "  Computer can combine 2-3 skill card"]
        self.level1_about = ["  < GAME RULE >", "  3 computer players", "  All cards equally divided except first card"]
        self.level2_about = ["  < GAME RULE >", "  2 computer players", "  Random color change every 5 turns"]
        self.level3_about = ["  < GAME RULE >", "", ""]
        self.levels_about = [self.level0_about, self.level1_about, self.level2_about,self.level3_about]
        if x + 310 > self.screen_width:
            self.about = pygame.Rect(x - 200, y - 100, 310, 100)
        self.about = pygame.Rect(x, y - 100, 310, 100)
        if x + 310 > self.screen_width:
            self.about.topright = (self.screen_width - 20, y - 100)
        pygame.draw.rect(screen, DARK_GRAY, self.about)


    def display_stage(self, screen):
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.img = pygame.transform.scale(pygame.image.load(resource_path("./assets/map.jpg")), (self.screen_width, self.screen_height))

        self.screen.blit(self.img, (0, 0))
        self.level0_txt.render(self.screen)
        self.level1_txt.render(self.screen)
        self.level2_txt.render(self.screen)
        self.level3_txt.render(self.screen)

        self.level0_rect.left = self.screen_width * 0.02
        self.level0_rect.top =self.screen_height * 0.75 - 150
        self.level1_rect.left = self.screen_width * 0.34
        self.level1_rect.top = self.screen_height * 0.45 - 150
        self.level2_rect.left = self.screen_width * 0.57
        self.level2_rect.top = self.screen_height * 0.75 - 130
        self.level3_rect.left = self.screen_width * 0.78
        self.level3_rect.top = self.screen_height * 0.45 - 150
        self.level_rects = [self.level0_rect, self.level1_rect, self.level2_rect, self.level3_rect]

        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.level_rects):
            if rect.collidepoint(mouse_pos):
                hover = pygame.transform.scale(
                        self.level_imgs[i], (rect.size[0]*1.2, rect.size[1]*1.2))
                self.screen.blit(hover, rect)
                self.about_stage(self.screen, rect.x, rect.y)
                for j in range(3):
                    text = self.font.render(self.levels_about[i][j], True, WHITE)
                    self.about.y = self.about.y + 22
                    screen.blit(text, self.about)
            else:
                self.screen.blit(self.level_imgs[i], rect)




    def running(self):

        self.display_stage(self.screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.level0_rect.collidepoint(event.pos):
                    return "game_level0"
                elif self.level1_rect.collidepoint(event.pos):
                    return "game_level1"
                elif self.level2_rect.collidepoint(event.pos):
                    return "game_level2"
                elif self.level3__rect.collidepoint(event.pos):
                    return "game_level3"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True
                    return "pause"


        pygame.display.update()
        return "map"
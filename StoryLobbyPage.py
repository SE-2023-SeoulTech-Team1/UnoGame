import pygame
from Button import Button
from Colors import *

fps = 60
fpsClock = pygame.time.Clock()

class StoryLobbyPage:
    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.game0 = False
        self.game1 = False
        self.game2 = False
        self.game3 = False

        self.key_idx = 0

        self.start_btn = Button(0.5, 0.3, 200, 50, 'START', text_size=32)
        self.start_btn.key_hovered = True
        self.map_btn = Button(0.5, 0.4, 200, 50, "MAP",text_size=32)
        self.exit_btn = Button(0.5, 0.5, 200, 50, 'EXIT', text_size=32)

        self.buttons = [self.start_btn, self.map_btn, self.exit_btn]
    

    def running(self, game_level):

        self.screen.fill(WHITE)
        self.game_level = game_level

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.rect.collidepoint(event.pos):
                    if self.game_level == 0:
                        return "game_level0"
                    elif self.game_level == 1:
                        return "game_level1"
                    elif self.game_level == 2:
                        return "game_level2"
                    elif self.game_level == 3:
                        return "game_level3"
                elif self.map_btn.rect.collidepoint(event.pos):
                    return "map"
                elif self.exit_btn.rect.collidepoint(event.pos):
                    return "exit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.key_idx += 1
                    self.key_idx %= len(self.buttons)
                    self.buttons[(self.key_idx - 1) % len(self.buttons)].key_hovered = False
                    self.buttons[self.key_idx].key_hovered = True
                elif event.key == pygame.K_UP:
                    self.key_idx -= 1
                    self.key_idx %= len(self.buttons)
                    self.buttons[(self.key_idx + 1) % len(self.buttons)].key_hovered = False
                    self.buttons[self.key_idx].key_hovered = True
                elif event.key == pygame.K_RETURN:
                    if self.key_idx == 0:
                        return "game_level0"
                    elif self.key_idx == 1:
                        return "map"
                    elif self.key_idx == 2:
                        return "exit"

        
        for button in self.buttons:
            button.process(self.screen)

        pygame.display.flip()
        fpsClock.tick(fps)

        if self.game_level == 0:
            return "story_lobby_0"
        elif self.game_level == 1:
            return "story_lobby_1"
        elif self.game_level == 2:
            return "story_lobby_2"
        elif self.game_level == 3:
            return "story_lobby_3"
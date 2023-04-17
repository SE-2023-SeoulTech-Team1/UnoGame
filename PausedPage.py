import pygame
import sys
from Colors import *
from Button import Button

class PausePage():
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.key_idx = 0

        self.pause_btn = Button(0.5, 0.3, 200, 50, "RESUME",text_size=40)
        self.pause_btn.key_hovered = True
        self.setting_btn = Button(0.5, 0.4, 200, 50, "SETTING",text_size=40)
        self.back_btn = Button(0.5, 0.5, 200, 50, "BACK",text_size=40)
        self.buttons = [self.pause_btn, self.setting_btn, self.back_btn]

    def running(self):

        self.screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_btn.rect.collidepoint(event.pos):
                    return "game"
                elif self.setting_btn.rect.collidepoint(event.pos):
                    return "setting"
                elif self.exit_btn.rect.collidepoint(event.pos):
                    return "main"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.key_idx += 1
                    self.key_idx %= len(self.buttons)
                    self.buttons[(self.key_idx - 1) % len(self.buttons)].key_hovered = False
                    self.buttons[self.key_idx].key_hovered = True
                elif event.key == pygame.K_UP:
                    # if self.key_idx > 0:
                    self.key_idx -= 1
                    self.key_idx %= len(self.buttons)
                    self.buttons[(self.key_idx + 1) % len(self.buttons)].key_hovered = False
                    self.buttons[self.key_idx].key_hovered = True
                elif event.key == pygame.K_RETURN:
                    if self.key_idx == 0:
                        return "game"
                    elif self.key_idx == 1:
                        return "setting"
                    elif self.key_idx == 2:
                        return "main"
       
        for button in self.buttons:
            button.process(self.screen)

        pygame.display.update()
        return "pause"

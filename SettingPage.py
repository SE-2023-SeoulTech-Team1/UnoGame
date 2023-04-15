import sys
import pygame
from Button import Button, Text
from Colors import *


class SettingPage():
    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.key_idx = 1

        self.screen_size_txt = Text(0.3, 0.3, 200, 50, 'screen size')
        self.color_weak_txt = Text(0.3, 0.4, 200, 50, 'color weak mode')
        self.key_txt = Text(0.3, 0.5, 200, 50, 'key')
        self.volume_txt = Text(0.3, 0.6, 200, 50, 'volume')
        self.reset_txt = Text(0.5, 0.7, 200, 50, 'RESET')
        self.back_txt = Text(0.5, 0.8, 200, 50, 'BACK')

        self.size_opt = {"idx": 0, "opt": ("800 x 600", "1000 x 750", "1200 x 900")}
        self.size_opt_btn = Button(0.7, 0.3, 200, 50, str(self.size_opt["opt"][self.size_opt["idx"]]))
        self.left_btn_0 = Text(0.55, 0.3, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_0 = Text(0.85, 0.3, 30, 30, '>', background_color=LIGHT_GRAY)

        self.color_weak_opt = {"idx": 0, "opt": ("off", "on")}
        self.color_weak_opt_btn = Button(0.7, 0.4, 200, 50, self.color_weak_opt["opt"][self.color_weak_opt["idx"]])
        self.left_btn_1 = Text(0.55, 0.4, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_1 = Text(0.85, 0.4, 30, 30, '>', background_color=LIGHT_GRAY)

        self.key_opt = {"idx": 0, "opt": ("mouse", "WSAD", "arrow keys")}
        self.key_opt_btn = Button(0.7, 0.5, 200, 50, self.key_opt["opt"][self.key_opt["idx"]])
        self.left_btn_2 = Text(0.55, 0.5, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_2 = Text(0.85, 0.5, 30, 30, '>', background_color=LIGHT_GRAY)

        self.volume_opt = {"idx": 0, "opt": ("a", "b", "c")}
        self.volume_opt_btn = Button(0.7, 0.6, 200, 50, self.volume_opt["opt"][self.volume_opt["idx"]])
        self.left_btn_3 = Text(0.55, 0.6, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_3 = Text(0.85, 0.6, 30, 30, '>', background_color=LIGHT_GRAY)

        self.opt_texts = [self.screen_size_txt, self.color_weak_txt,
                        self.key_txt, self.volume_txt, self.reset_txt, self.back_txt]
        self.opt = [self.size_opt, self.color_weak_opt, self.key_opt, self.volume_opt]
        self.opt_buttons = [self.size_opt_btn, self.color_weak_opt_btn, self.key_opt_btn, self.volume_opt_btn]
        self.left_buttons = [self.left_btn_0, self.left_btn_1, self.left_btn_2, self.left_btn_3]
        self.right_buttons = [self.right_btn_0, self.right_btn_1, self.right_btn_2, self.right_btn_3]

    def go_to_back(self):
        print("go to back")


    def size_setting(self):
        print("size_setting!!")
        pass


    def set_screen_size(self, screen_width, screen_height):
        pygame.display.set_mode((screen_width, screen_height))
        pass


    def key_setting(self):
        print("key_setting!!")
        pass


    def colorblind_setting(self):
        print("colorblind_setting!!")
        pass


    def volume_setting(self):
        print("volume_setting!!")
        pass


    def reset_setting(self):
        print("reset_setting!!")
        pass


    def running(self):
        self.screen.fill(WHITE)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            elif event.type == pygame.MOUSEBUTTONDOWN:

                for key_idx, left_button in enumerate(self.left_buttons):
                    self.key_idx = key_idx
                    if left_button.rect.collidepoint(event.pos):
                        self.opt[self.key_idx]["idx"] -= 1
                        self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                        self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]
                for key_idx, right_button in enumerate(self.right_buttons):
                    self.key_idx = key_idx
                    if right_button.rect.collidepoint(event.pos):
                        self.opt[self.key_idx]["idx"] += 1
                        self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                        self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]

                if self.back_txt.rect.collidepoint(event.pos):
                    return "main"

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    self.key_idx += 1
                    self.key_idx %= len(self.opt_buttons)
                    self.opt_buttons[(self.key_idx - 1) %  len(self.opt_buttons)].key_hovered = False
                    self.opt_buttons[self.key_idx].key_hovered = True

                elif event.key == pygame.K_UP:
                    self.key_idx -= 1
                    self.key_idx %= len(self.opt_buttons)
                    self.opt_buttons[(self.key_idx + 1) %  len(self.opt_buttons)].key_hovered = False
                    self.opt_buttons[self.key_idx].key_hovered = True

                elif event.key == pygame.K_LEFT:
                    self.opt[self.key_idx]["idx"] -= 1
                    self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                    self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]

                elif event.key == pygame.K_RIGHT:
                    self.opt[self.key_idx]["idx"] += 1
                    self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                    self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]

                elif event.key == pygame.K_RETURN:
                    # if self.key_idx == 0:
                    #     pygame.display.set_mode((800, 600))
                    # elif self.key_idx == 1:
                    #     pygame.display.set_mode((1000, 750))
                    # elif self.key_idx == 2:
                    #     pygame.display.set_mode((1200, 900))
                    if self.key_idx == len(self.buttons) - 1:
                        return "main"

        for button in (self.opt_texts + self.opt_buttons + self.left_buttons + self.right_buttons):
            button.process(self.screen)

        pygame.display.flip()
        fpsClock.tick(fps)
        return "setting"

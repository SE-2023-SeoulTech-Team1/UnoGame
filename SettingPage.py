import sys
import pygame
from Button import Button, TextButton, Slider
from Colors import *
import pickle
import os 

class SettingPage():
    def __init__(self, screen, setting):
        # 출력 Test 
        print("setting volume : " + str(setting.volume))
        print("key : " + str(setting.key))
        print("colorweak : " + str(setting.color_weak))
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.key_idx = 0
        if os.path.exists("../setting_state.pkl"):
            self.size_idx = setting.size_idx
            self.color_idx = setting.color_idx
            self.keys_idx = setting.keys_idx
            # print("size_idx : " + str(setting.size_idx))
        else:
            self.size_idx = 0
            self.color_idx = 0
            self.keys_idx = 0
        
        self.screen_size_txt = TextButton(0.3, 0.2, 200, 50, 'screen size')
        self.color_weak_txt = TextButton(0.3, 0.3, 200, 50, 'color weak mode')
        self.key_txt = TextButton(0.3, 0.4, 200, 50, 'key')
        self.volume_txt = TextButton(0.3, 0.5, 200, 50, 'vol.')
        self.back_volume_txt = TextButton(0.3, 0.6, 200, 50, 'background vol.')
        self.effect_volume_txt = TextButton(0.3, 0.7, 200, 50, 'effect vol.')
        self.save_txt = TextButton(0.25, 0.85, 200, 50, 'SAVE')
        self.reset_txt = TextButton(0.5, 0.85, 200, 50, 'RESET')
        self.back_txt = TextButton(0.75, 0.85, 200, 50, 'BACK')

        self.size_opt = {"idx": self.size_idx, "opt": ("800 x 600", "1000 x 750", "1200 x 900")}
        self.size_opt_btn = Button(0.7, 0.2, 200, 50, str(self.size_opt["opt"][self.size_opt["idx"]]))
        self.left_btn_0 = TextButton(0.55, 0.2, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_0 = TextButton(0.85, 0.2, 30, 30, '>', background_color=LIGHT_GRAY)

        self.color_weak_opt = {"idx": self.color_idx, "opt": ("off", "on")}
        self.color_weak_opt_btn = Button(0.7, 0.3, 200, 50, self.color_weak_opt["opt"][self.color_weak_opt["idx"]])
        self.left_btn_1 = TextButton(0.55, 0.3, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_1 = TextButton(0.85, 0.3, 30, 30, '>', background_color=LIGHT_GRAY)

        self.key_opt = {"idx":self.keys_idx, "opt": ("mouse", "WSAD", "arrow keys")}
        self.key_opt_btn = Button(0.7, 0.4, 200, 50, self.key_opt["opt"][self.key_opt["idx"]])
        self.left_btn_2 = TextButton(0.55, 0.4, 30, 30, '<', background_color=LIGHT_GRAY)
        self.right_btn_2 = TextButton(0.85, 0.4, 30, 30, '>', background_color=LIGHT_GRAY)

        self.volume_slider = Slider(0.7, 0.5, 200, 50, setting.volume)
        self.back_volume_slider = Slider(0.7, 0.6, 200, setting.back_volume)
        self.effect_volume_slider = Slider(0.7, 0.7, 200, 50, setting.effect_volume)

        self.opt_texts = [self.screen_size_txt, self.color_weak_txt, self.key_txt, 
                    self.volume_txt, self.back_volume_txt, self.effect_volume_txt,
                    self.save_txt, self.reset_txt, self.back_txt]
        # 3가지 모음 
        self.opt = [self.size_opt, self.color_weak_opt, self.key_opt]
        self.opt_buttons = [self.size_opt_btn, self.color_weak_opt_btn, self.key_opt_btn]
        self.left_buttons = [self.left_btn_0, self.left_btn_1, self.left_btn_2]
        self.right_buttons = [self.right_btn_0, self.right_btn_1, self.right_btn_2]
        self.volume_sliders = [self.volume_slider, self.back_volume_slider, self.effect_volume_slider]
       
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
                        # print("left button click : " + str(self.opt[self.key_idx]["idx"]))
                for key_idx, right_button in enumerate(self.right_buttons):
                    self.key_idx = key_idx
                    if right_button.rect.collidepoint(event.pos):
                        self.opt[self.key_idx]["idx"] += 1
                        self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                        self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]
                
                for slider in self.volume_sliders:
                    if event.pos[0] >= slider.top and event.pos[0] <= slider.top + slider.length and event.pos[1] >= slider.left - 10 and event.pos[1] <= slider.left + 10:
                        slider.value = int((event.pos[0] - slider.top) / slider.length * (slider.max_val - slider.min_val) + slider.min_val)

                if self.save_txt.rect.collidepoint(event.pos):
                    width, height = self.size_opt_btn.text.split(' x ')
                    screen_size = (int(width), int(height))
                    color_weak = True if self.color_weak_opt_btn.text == "on" else False
                    key = self.key_opt_btn.text
                    volumn = self.volume_slider.value
                    back_volumn = self.back_volume_slider.value
                    effect_volumn = self.effect_volume_slider.value
                    self.setting.set(screen_size, color_weak, key, volumn, back_volumn, effect_volumn, self.opt[0]["idx"], self.opt[1]["idx"], self.opt[2]["idx"])
                    setting2 = self.setting

                    # pickle에 현재 데이터 저장 
                    with open("../setting_state.pkl", "wb") as f:
                        pickle.dump(setting2, f)
                    return "main"

                elif self.reset_txt.rect.collidepoint(event.pos):
                    self.size_opt_btn.text = "800 x 600"
                    self.color_weak_opt_btn.text = "off"
                    self.key_opt_btn.text = "mouse"
                        
                    self.volume_slider.value = 50
                    self.back_volume_slider.value = 50
                    self.effect_volume_slider.value = 50
                    self.setting.reset()
                    setting2 = self.setting
                    with open("../setting_state.pkl", "wb") as f:
                        pickle.dump(setting2, f)
                    return "main"

                elif self.back_txt.rect.collidepoint(event.pos):
                    return "main"

            elif event.type == pygame.KEYDOWN:
                buttons_with_keyboard = self.opt_buttons + self.opt_texts[4:]
                if event.key == pygame.K_DOWN:
                    self.key_idx += 1
                    self.key_idx %= len(buttons_with_keyboard)
                    buttons_with_keyboard[(self.key_idx - 1) % len(buttons_with_keyboard)].key_hovered = False
                    buttons_with_keyboard[self.key_idx].key_hovered = True

                elif event.key == pygame.K_UP:
                    self.key_idx -= 1
                    self.key_idx %= len(buttons_with_keyboard)
                    buttons_with_keyboard[(self.key_idx + 1) % len(buttons_with_keyboard)].key_hovered = False
                    buttons_with_keyboard[self.key_idx].key_hovered = True

                elif event.key == pygame.K_LEFT and self.key_idx < len(self.opt_buttons):
                    self.opt[self.key_idx]["idx"] -= 1
                    self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                    self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]

                elif event.key == pygame.K_RIGHT and self.key_idx < len(self.opt_buttons):
                    self.opt[self.key_idx]["idx"] += 1
                    self.opt[self.key_idx]["idx"] %= len(self.opt[self.key_idx]["opt"])
                    self.opt_buttons[self.key_idx].text = self.opt[self.key_idx]["opt"][self.opt[self.key_idx]["idx"]]

                elif event.key == pygame.K_RETURN:
                    if self.key_idx == 4:
                        width, height = self.size_opt_btn.text.split(' x ')
                        screen_size = (int(width), int(height))
                        color_weak = True if self.color_weak_opt_btn.text == "on" else False
                        key = self.key_opt_btn.text
                        self.setting.set(screen_size, color_weak, key)
                        return "main"

                    elif self.key_idx == 5:
                        self.setting.reset()
                        return "main"

                    if self.key_idx == len(buttons_with_keyboard) - 1:
                        return "main"

        for button in (self.opt_texts + self.opt_buttons + self.left_buttons + self.right_buttons):
            button.process(self.screen)

        for slider in self.volume_sliders:
            slider.process_slider(self.screen)

        pygame.display.flip()
        fpsClock.tick(fps)
        return "setting"

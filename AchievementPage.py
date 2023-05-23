import pygame
import pygame_gui
import pickle
import os
from Achievement import Achievement
from resource_path import *
from Colors import *

class AchievementPage:

    def __init__(self, screen, setting):
        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.setting = setting
        self.single_medal_img =  pygame.image.load(resource_path("./assets/single_medal.png"))
        self.level0_medal_img =  pygame.image.load(resource_path("./assets/level0_medal.png"))
        self.level1_medal_img =  pygame.image.load(resource_path("./assets/level1_medal.png"))
        self.level2_medal_img =  pygame.image.load(resource_path("./assets/level2_medal.png"))
        self.level3_medal_img =  pygame.image.load(resource_path("./assets/level3_medal.png"))      
        self.turn10_medal_img =  pygame.image.load(resource_path("./assets/10turn_medal.png"))
        self.turn15_medal_img =  pygame.image.load(resource_path("./assets/15turn_medal.png"))
        self.turn20_medal_img =  pygame.image.load(resource_path("./assets/20turn_medal.png"))
        self.skill_medal_img =  pygame.image.load(resource_path("./assets/skill_medal.png"))
        self.uno_medal_img =  pygame.image.load(resource_path("./assets/uno_medal.png"))
        self.medal_imgs = [self.single_medal_img, self.level0_medal_img, self.level1_medal_img, self.level2_medal_img,
                            self.level3_medal_img, self.turn10_medal_img, self.turn15_medal_img, self.turn20_medal_img,
                            self.skill_medal_img, self.uno_medal_img]
        if os.path.exists('achievements.pkl'):
            with open('achievements.pkl', 'rb') as f:
                self.achievements = pickle.load(f)
                print("achievements 실행")
        else:
            self.achievements = [
                Achievement("Win Single Player Game", "Win a single player game"),
                Achievement("Win Story Game(level0)", "Win a story game(level0)"),
                Achievement("Win Story Game(level1)", "Win a story game(level1)"),
                Achievement("Win Story Game(level2)", "Win a story game(level2)"),
                Achievement("Win Story Game(level3)", "Win a story game(level3)"),
                Achievement("In 10 turns", "Win a single player game in 10 turns"),
                Achievement("In 15 turns", "Win a single player game in 15 turns"),
                Achievement("In 20 turns", "Win a single player game in 20 turns"),
                Achievement("Win without skill cards", "Win a single player game without using skill cards"),
                Achievement("Win without uno button", "Win a single player game without using uno button"),
            ]
        # self.achievements[0].complete()

    def running(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill(WHITE)
            for i, achievement in enumerate(self.achievements):
                achievement.draw(self.screen, (i + 1) * 0.08)
            for i, img in enumerate(self.medal_imgs):
                img_rect = img.get_rect()
                img = pygame.transform.scale(
                    img, (img_rect.size[0] * 0.2, img_rect.size[1] * 0.2))
                img_rect.x = self.screen_width * 0.08
                img_rect.y = self.screen_height * (i + 1) * 0.08
                self.screen.blit(img, img_rect)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                        return "pause"
            pygame.display.flip()

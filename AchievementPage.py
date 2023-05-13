import pygame
import pickle
import os
from Achievement import Achievement
from Colors import *

class AchievementPage:

    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting
        if os.path.exists('achievements.pickle'):
            with open('achievements.pickle', 'rb') as f:
                self.achievements = pickle.load(f)
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

    def running(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill(WHITE)
            for i, achievement in enumerate(self.achievements):
                achievement.draw(self.screen, (i + 1) * 0.1)
            pygame.display.flip()

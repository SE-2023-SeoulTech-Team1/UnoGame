import pygame

class Setting():
    def __init__(self):
        self.screen_size = (800, 600)
        self.color_weak = False
        self.key = "mouse"
        self.volume = "a"

    def reset(self):
        self.screen_size = (800, 600)
        pygame.display.set_mode(self.screen_size)
        self.color_weak = False
        self.key = "mouse"
        self.volume = "a"

    def set(self, screen_size, color_weak, key, volume):
        """
        setting.set()을 통해 모든 세팅을 변경
        """
        self.screen_size = screen_size
        pygame.display.set_mode(self.screen_size)
        self.color_weak = color_weak
        self.key = key
        self.volume = volume
import pygame

class Setting():
    def __init__(self):
        self.screen_size = (800, 600)
        self.color_weak = False
        self.key = "mouse"
        self.volume = 50
        self.back_volume = 50
        self.effect_volume = 50
        self.keys_idx = 0
        self.size_idx = 0
        self.color_idx = 0

    def reset(self):
        self.screen_size = (800, 600)
        pygame.display.set_mode(self.screen_size)
        self.color_weak = False
        self.key = "mouse"
        self.volume = 50
        self.back_volume = 50
        self.effect_volume = 50
        self.keys_idx = 0
        self.size_idx = 0
        self.color_idx = 0

    def set(self,screen_size, color_weak, key, volume, back_volume, effect_volume, size_idx, color_idx, keys_idx):
        """
        setting.set()을 통해 모든 세팅을 변경
        """

        self.screen_size = screen_size
        pygame.display.set_mode(self.screen_size)
        self.color_weak = color_weak
        self.key = key
        self.volume = volume
        self.back_volume = back_volume
        self.effect_volume = effect_volume
        self.keys_idx = keys_idx
        self.size_idx = size_idx
        self.color_idx = color_idx
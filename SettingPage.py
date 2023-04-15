import sys
import pygame
from Button import Button

fps = 60
fpsClock = pygame.time.Clock()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont(None, 30)


class SettingPage():
    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()

        self.size1_btn = Button(0.5, 0.1, 200, 50, '800 x 600')
        self.size2_btn = Button(0.5, 0.2, 200, 50, '1000 x 750')
        self.size3_btn = Button(0.5, 0.3, 200, 50, '1200 x 900')

        self.color_weak_btn = Button(0.5, 0.4, 200, 50, 'colorblind')
        self.key_btn = Button(0.5, 0.5, 200, 50, 'key')
        self.volume_btn = Button(0.5, 0.6, 200, 50, 'volume')
        self.reset_btn = Button(0.5, 0.7, 200, 50, 'reset')
        self.back_btn = Button(0.5, 0.8, 200, 50, 'BACK')


        self.buttons = [self.color_weak_btn, self.key_btn, self.volume_btn, self.reset_btn,
                        self.back_btn, self.size1_btn, self.size2_btn, self.size3_btn]

        self.color_weak = False
        self.volume = None

    def go_to_back(self):
        print("go to back")


    def size_setting(self):
        print("size_setting!!")
        pass


    # 화면 비율을 변경하는 함수
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
                print(event.pos)

                if self.size1_btn.rect.collidepoint(event.pos):
                    pygame.display.set_mode((800, 600))

                elif self.size2_btn.rect.collidepoint(event.pos):
                    pygame.display.set_mode((1000, 750))

                elif self.size3_btn.rect.collidepoint(event.pos):
                    pygame.display.set_mode((1200, 900))

                elif self.color_weak_btn.rect.collidepoint(event.pos):
                    self.color_weak_btn.clicked()

                elif self.key_btn.rect.collidepoint(event.pos):
                    self.key_btn.clicked()

                elif self.volume_btn.rect.collidepoint(event.pos):
                    self.volume_btn.clicked()

                elif self.reset_btn.rect.collidepoint(event.pos):
                    self.reset_btn.clicked()

                elif self.back_btn.rect.collidepoint(event.pos):
                    return "main"

        for button in self.buttons:
            button.process(self.screen)

        pygame.display.flip()
        fpsClock.tick(fps)
        return "setting"
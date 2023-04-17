import pygame
from Button import Button, TextButton

fps = 60
fpsClock = pygame.time.Clock()

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont('arialroundedmtbold', 48)


class MainPage():
    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.title = TextButton(1/2, 1/6, 200, 50, "UNO GAME", hover_color=WHITE, text_color=BLUE)

        self.key_idx = 0
        self.start_btn = Button(0.5, 0.3, 200, 50, 'START', text_size=32)
        self.start_btn.key_hovered = True
        self.map_btn = Button(0.5, 0.4, 200, 50, 'GO TO MAP', text_size=32)
        self.setting_btn = Button(0.5, 0.5, 200, 50, 'SETTINGS', text_size=32)
        self.exit_btn = Button(0.5, 0.6, 200, 50, 'EXIT', text_size=32)

        self.buttons = [self.start_btn, self.map_btn, self.setting_btn, self.exit_btn]


    def running(self):

        self.screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.rect.collidepoint(event.pos):
                    return "game"
                if self.map_btn.rect.collidepoint(event.pos):
                    return "map"
                if self.setting_btn.rect.collidepoint(event.pos):
                    return "setting"
                if self.exit_btn.rect.collidepoint(event.pos):
                    return "exit"

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
                        return "map"
                    elif self.key_idx == 2:
                        return "setting"
                    elif self.key_idx == 3:
                        return "exit"

        self.title.process(self.screen)
        for button in self.buttons:
            button.process(self.screen)

        # 화면 업데이트
        pygame.display.flip()
        fpsClock.tick(fps)
        return "main"
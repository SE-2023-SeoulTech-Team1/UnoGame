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
font = pygame.font.SysFont(None, 48)


# Title 클래스 
class Title():
    def __init__(self, x, y, text = 'title'):
        self.x = x
        self.y = y
    
        self.fillColors = {
            'normal': '#A5140C',
        }
        self.titleText = font.render(text, True, BLUE)

    def process(self, screen):
        screen.blit(self.titleText, [self.x, self.y])


class MainPage():
    def __init__(self, screen):

        self.screen = screen
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # 초기 페이지 상태
        self.next_page = False
        self.key_idx = 0
        self.screenPage = False

        # self.start_btn = Button((self.screen_width - 200) / 2, 150, 200, 50, 'START', self.startFunction)
        # self.setting_btn = Button((self.screen_width - 200) / 2, 230, 200, 50, 'SETTINGS', self.settingFunction)
        # self.exit_btn = Button((self.screen_width - 200) / 2, 310, 200, 50, 'EXIT', self.exitFunction)
        # self.start_btn = Button((self.screen_width - 200) / 2, 150, 200, 50, 'START')
        self.start_btn = Button(1/2, 1/6, 200, 50, 'START')
        self.setting_btn = Button(1/2, 3/6, 200, 50, 'SETTINGS')
        self.exit_btn = Button(1/2, 5/6, 200, 50, 'EXIT')
        self.titleObjects = [Title(310, 50, 'UNO GAME')]

        self.buttons = []
        self.buttons.append(self.start_btn)
        self.buttons.append(self.setting_btn)
        self.buttons.append(self.exit_btn)

    # def update_screen_size(self):


    def running(self):

        self.screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_btn.rect.collidepoint(event.pos):
                    return "game"
                if self.setting_btn.rect.collidepoint(event.pos):
                    return "setting"
                if self.exit_btn.rect.collidepoint(event.pos):
                    return "exit"

        for button in self.buttons:
            button.process(self.screen)

        # 화면 업데이트
        pygame.display.flip()
        fpsClock.tick(fps)
        return "main"

                # if self.setting_btn.buttonRect.collidepoint(mousePos) and self.next_page == False:
                #     self.changeFunction()
                #     self.next_page = True
                #     self.key_idx = 3
                # elif self.back_btn1.buttonRect.collidepoint(mousePos):
                #     self.changeFunction()
                #     self.next_page = False
                #     self.key_idx = 0
                # elif self.size_btn.buttonRect.collidepoint(mousePos) and self.screenPage == False:
                #     self.size_setting()
                #     self.screenPage = True
                #     self.key_idx = 9
                # elif self.back_btn2.buttonRect.collidepoint(mousePos):
                #     self.size_setting()
                #     self.screenPage = False
                #     self.key_idx = 3


        #     if event.type == pygame.KEYDOWN:
        #         if self.next_page == False and self.screenPage == False:
        #             if event.key == pygame.K_DOWN:
        #                 if self.key_idx < 2:
        #                     self.key_idx += 1
        #             elif event.key == pygame.K_UP:
        #                 if self.key_idx > 0:
        #                     self.key_idx -= 1
        #             elif event.key == pygame.K_RETURN:
        #                 if self.key_idx == 0:
        #                     self.startFunction()
        #                 elif self.key_idx == 1:
        #                     self.settingFunction()
        #                 elif self.key_idx == 2:
        #                     self.exitFunction()
        #         elif self.next_page == True and self.screenPage == False:
        #             if event.key == pygame.K_DOWN:
        #                 if self.key_idx < 8:
        #                     self.key_idx += 1
        #             elif event.key == pygame.K_UP:
        #                 if self.key_idx > 3:
        #                     self.key_idx -= 1
        #             elif event.key == pygame.K_RETURN:
        #                 if self.key_idx == 3:
        #                     self.size_setting()
        #                 elif self.key_idx == 4:
        #                     self.colorblind_setting()
        #                 elif self.key_idx == 5:
        #                     self.key_setting()
        #                 elif self.key_idx == 6:
        #                     self.volume_setting()
        #                 elif self.key_idx == 7:
        #                     self.reset_setting()
        #                 elif self.key_idx == 8:
        #                     self.next_page = False
        #                     self.key_idx = 1
        #         elif self.next_page == True and self.screenPage == True:
        #             if event.key == pygame.K_DOWN:
        #                 if self.key_idx < 12:
        #                     self.key_idx += 1
        #             elif event.key == pygame.K_UP:
        #                 if self.key_idx > 9:
        #                     self.key_idx -= 1
        #             elif event.key == pygame.K_RETURN:
        #                 if self.key_idx == 9:
        #                     self.set_screen_size(800, 600)
        #                 elif self.key_idx == 10:
        #                     self.set_screen_size(1024, 768)
        #                 elif self.key_idx == 11:
        #                     self.set_screen_size(1280, 720)
        #                 elif self.key_idx == 12:
        #                     self.screenPage = False
        #                     self.key_idx = 3
        # # 객체들 처리
        # if self.next_page == False and self.screenPage == False:
        #     self.titleObjects[0].process(self.screen)
        #     for button in self.buttons[0:3]:
        #         button.process(self.screen)
        #         if self.key_idx == self.buttons.index(button):
        #             button.process(self.screen, hover=True)
        # elif self.next_page == True and self.screenPage == False:
        #     for button in self.buttons[3:9]:
        #         button.process(self.screen, hover=True)
        #         if self.key_idx == self.buttons.index(button):
        #             button.process(self.screen)
        # elif self.next_page == True and self.screenPage == True:
        #     for button in self.buttons[9:]:
        #         button.process(self.screen, hover=True)
        #         if self.key_idx == self.buttons.index(button):
        #             button.process(self.screen)

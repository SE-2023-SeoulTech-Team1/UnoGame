import pygame
import sys

# 게임 윈도우 초기화
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Uno Game")

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

titleObjects = []
objects = []

# Button 클래스 
class Button():
    def __init__(self, x,  y, width, height, buttonText = 'Button', onclickFunction = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#A5140C',
            'hover': '#820600',
            'pressed': '#570400',
            'drop_normal': '#'
        }
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonText = font.render(buttonText, True, BLACK)
        objects.append(self) # object 리스트에 버튼 인스턴스를 추가

    def process(self, ini = None):
        self.ini = ini
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]: # 왼쪽 마우스 버튼이 눌렸으면
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        if ini == True:
            self.buttonSurface.fill(self.fillColors['hover'])

        # Surface에 텍스트 위치 시킴 
        self.buttonSurface.blit(self.buttonText, [
            self.buttonRect.width/2 - self.buttonText.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonText.get_rect().height/2
        ])
        # screen에 Surface 위치 시킴 
        screen.blit(self.buttonSurface, self.buttonRect)

# Title 클래스 
class Title():
    def __init__(self, x, y, text = 'title'):
        self.x = x
        self.y = y
    
        self.fillColors = {
            'normal': '#A5140C',
        }
        self.titleText = font.render(text, True, BLUE)
        titleObjects.append(self)

    def process(self):
        screen.blit(self.titleText, [self.x, self.y])


class SettingPage():
    def __init__(self):
        self.create_buttons()
        self.create_title()
    
    def create_title(self):
        Title(330, 50, 'Settings')

    def create_buttons(self):
        size_btn = Button(300, 150, 200, 50, 'Screen Size', self.size_setting)
        key_btn = Button(300, 230, 200, 50, 'Key Setting', self.key_setting)
        color_btn = Button(300, 310, 200, 50, 'Color Blind Mode', self.colorblind_setting)
        volume_btn = Button(300, 390, 200, 50, 'Volume', self.volume_setting)
        back_btn = Button(325, 470, 150, 50, 'BACK', self.back_setting)


    def size_setting(self):
        pass

    def key_setting(self):
        pass

    def colorblind_setting(self):
        pass

    def volume_setting(self):
        pass

    def back_setting(self):
        global nextPage
        nextPage = True

def startSettingPage():
    
    settingPage = SettingPage()
    while not nextPage:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(WHITE)
        for obj in titleObjects:
            obj.process()
        for obj in objects:
            obj.process()
        pygame.display.update()
        fpsClock.tick(fps)

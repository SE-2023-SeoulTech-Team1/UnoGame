import pygame
import sys
from GamePage import startGamePage

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


def startFunction():
    print("startFunction!!") 
    startGamePage()

def settingFunction():
    print("settingFunction!!")
    changeFunction()


def exitFunction():
    print("exitFunction!!")
    pygame.quit()
    sys.exit()

def size_setting():
    print("size_setting!!")
    pass


# 1번 함수 구현
def size_setting():
    global screenPage, key_idx
    if screenPage:
        screenPage = False
        key_idx = 3
    else:
        screenPage = True
        key_idx = 9
    



# 화면 비율을 변경하는 함수
def set_screen_size(screen_width, screen_height):
    screen_width, screen_height  
    pygame.display.set_mode((screen_width, screen_height))
    
    
    
def key_setting():
    print("key_setting!!")
    pass
    

def colorblind_setting():
    print("colorblind_setting!!")
    pass

def volume_setting():
    print("volume_setting!!")
    pass

def reset_setting():
    print("reset_setting!!")
    pass


def changeFunction():
    global nextPage, key_idx
    if nextPage:
        nextPage = False
        key_idx = 1
    else:
        nextPage = True
        key_idx = 3
    print("changeFunction!!")

screen_size = (800, 600)


titleObjects = [Title(310, 50, 'UNO GAME')]

start_btn = Button((screen_width-200)/2, 150, 200, 50, 'START', startFunction)
setting_btn = Button((screen_width-200)/2, 230, 200, 50, 'SETTINGS', settingFunction)
exit_btn = Button((screen_width-200)/2, 310, 200, 50, 'EXIT', exitFunction)
size_btn = Button((screen_width-200)/2, 50, 200, 50, 'screen size', size_setting)
color_btn = Button((screen_width-200)/2, 130, 200, 50, 'colorblind', colorblind_setting)
key_btn = Button((screen_width-200)/2, 210, 200, 50, 'key', key_setting)
volume_btn = Button((screen_width-200)/2, 290, 200, 50, 'volume', volume_setting)
reset_btn = Button((screen_width-200)/2, 370, 200, 50, 'reset', reset_setting)
back_btn1 = Button((screen_width-150)/2, 450, 150, 50, 'BACK', changeFunction)
size1_btn = Button((screen_width-200)/2, 50, 200, 50, '800 x 600', set_screen_size(800 , 600))
size2_btn = Button((screen_width-200)/2, 130, 200, 50, '1024 x 768', set_screen_size(1024, 768))
size3_btn = Button((screen_width-200)/2, 210, 200, 50, '1280 x 720', set_screen_size(1280 , 720))
back_btn2 = Button((screen_width-150)/2, 290, 150, 50, 'BACK', size_setting)


# 초기 페이지 상태
nextPage = False
key_idx = 0
screenPage = False


# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if setting_btn.buttonRect.collidepoint(mousePos) and nextPage == False:
                changeFunction()
                nextPage = True
                key_idx = 3
            elif back_btn1.buttonRect.collidepoint(mousePos):
                changeFunction()
                nextPage = False
                key_idx = 0
            elif size_btn.buttonRect.collidepoint(mousePos) and screenPage == False:
                size_setting()
                screenPage = True
                key_idx = 9
            elif back_btn2.buttonRect.collidepoint(mousePos):
                size_setting()
                screenPage = False
                key_idx = 3


        if event.type == pygame.KEYDOWN:
            if nextPage == False and screenPage == False:
                if event.key == pygame.K_DOWN:
                    if key_idx < 2:
                        key_idx += 1
                elif event.key == pygame.K_UP:
                    if key_idx > 0:
                        key_idx -= 1
                elif event.key == pygame.K_RETURN:
                    if key_idx == 0:
                        startFunction()
                    elif key_idx == 1:
                        settingFunction()
                    elif key_idx == 2:
                        exitFunction()
            elif nextPage == True and screenPage == False:
                if event.key == pygame.K_DOWN:
                    if key_idx < 8:
                        key_idx += 1
                elif event.key == pygame.K_UP:
                    if key_idx > 3:
                        key_idx -= 1
                elif event.key == pygame.K_RETURN:
                    if key_idx == 3:
                        size_setting()
                    elif key_idx == 4:
                        colorblind_setting()
                    elif key_idx == 5:
                        key_setting()
                    elif key_idx == 6:
                        volume_setting()
                    elif key_idx == 7:
                        reset_setting()
                    elif key_idx == 8:
                        nextPage = False
                        key_idx = 1
            elif nextPage == True and screenPage == True:
                if event.key == pygame.K_DOWN:
                    if key_idx < 12:
                        key_idx += 1
                elif event.key == pygame.K_UP:
                    if key_idx > 9:
                        key_idx -= 1
                elif event.key == pygame.K_RETURN:
                    if key_idx == 9:
                        set_screen_size(800, 600)
                    elif key_idx == 10:
                        set_screen_size(1024, 768)
                    elif key_idx == 11:
                        set_screen_size(1280, 720)
                    elif key_idx == 12:
                        screenPage = False
                        key_idx = 3
    # 객체들 처리
    if nextPage == False and screenPage == False:
        titleObjects[0].process()
        for object in objects[0:3]:
            object.process()
            if key_idx == objects.index(object):
                object.process(True)
    elif nextPage == True and screenPage == False:
        for object in objects[3:9]:
            object.process()
            if key_idx == objects.index(object):
                object.process(True)
    elif nextPage == True and screenPage == True:
        for object in objects[9:]:
            object.process()
            if key_idx == objects.index(object):
                object.process(True)
        

    # 화면 업데이트
    pygame.display.flip()
    fpsClock.tick(fps)

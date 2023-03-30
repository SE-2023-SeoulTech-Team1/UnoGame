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

nextPage = False

def startFunction():
    print("startFunction!!") 
    startGamePage()

def startFunction2():
    print("startFunction2!!")   
    
def settingFunction():
    print("settingFunction!!")

def exitFunction():
    print("exitFunction!!")
    pygame.quit()
    sys.exit()
    
def changeFunction():
    objects[0], objects[4] = objects[4], objects[0] 
    objects[1], objects[5] = objects[5], objects[1] 
    objects[2], objects[6] = objects[6], objects[2]

# 타이틀 생성 
Title(310, 50, 'UNO GAME')

# 버튼 생성
start_btn = Button(300, 150, 200, 50, 'START', startFunction)
setting_btn = Button(300, 230, 200, 50, 'SETTINGS', settingFunction)
exit_btn = Button(300, 310, 200, 50, 'EXIT', exitFunction)
back_btn = Button(325, 390, 150, 50, 'BACK', changeFunction)
Button5 = Button(300, 150, 200, 50, 'START2', startFunction2)
Button6 = Button(300, 230, 200, 50, 'SETTINGS2', settingFunction)
Button7 = Button(300, 310, 200, 50, 'EXIT2', exitFunction)


key_idx = 0
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
                nextPage = False if nextPage else True
            elif back_btn.buttonRect.collidepoint(mousePos):
                changeFunction()
                nextPage = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_DOWN:
                if key_idx < 4:
                    key_idx += 1
            elif event.key == pygame.K_UP:
                if key_idx >= 0:
                    key_idx -= 1
            elif event.key == pygame.K_RETURN:
                objects[key_idx].onclickFunction()
                if key_idx == 1 and nextPage == False:
                    changeFunction()
                    if nextPage == True:
                        nextPage = False
                    elif nextPage == False:
                        nextPage = True
                if key_idx == 3:
                    nextPage = False
                    key_idx = 1
                

    titleObjects[0].process()
    for object in objects[0:3]:
        object.process()
        if key_idx == 0:
            objects[key_idx].process(True)
        if key_idx == 1:
            objects[key_idx].process(True)
        if key_idx == 2:
            objects[key_idx].process(True)
        if nextPage == True:
            objects[3].process()
            if key_idx == 3:
                objects[key_idx].process(True)


    pygame.display.flip()
    fpsClock.tick(fps)
import pygame
import sys
# from SettingPage import draw_settings_screen

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
        objects.append(self)

    def process(self, ini = None):
        self.ini = ini
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
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
def startFunction2():
    print("startFunction2!!")   
    
def settingFunction():
    print("settingFunction!!")
def exitFunction():
    print("exitFunction!!")
    pygame.quit()
    sys.exit()
def backFunction():
    objects[0], objects[4] = objects[4], objects[0] 
    objects[1], objects[5] = objects[5], objects[1] 
    objects[2], objects[6] = objects[6], objects[2] 
    nextPage = False

# 타이틀 생성 
Title(310, 50, 'UNO GAME')
# 버튼 생성 

Button1 = Button(300, 150, 200, 50, 'START', startFunction)
Button2 = Button(300, 230, 200, 50, 'SETTINGS', settingFunction)
Button3 = Button(300, 310, 200, 50, 'EXIT', exitFunction)
Button4 = Button(325, 390, 150, 50, 'BACK', backFunction)
Button5 = Button(300, 150, 200, 50, 'START2', startFunction2)
Button6 = Button(300, 230, 200, 50, 'SETTINGS2', settingFunction)
Button7 = Button(300, 310, 200, 50, 'EXIT2', exitFunction)


i = 0
# 메인 루프
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if Button2.buttonRect.collidepoint(mousePos) and nextPage == False:
                objects[0], objects[4] = objects[4], objects[0] 
                objects[1], objects[5] = objects[5], objects[1] 
                objects[2], objects[6] = objects[6], objects[2] 
                if nextPage == True:
                    nextPage = False
                elif nextPage == False:
                    nextPage = True
            elif Button4.buttonRect.collidepoint(mousePos):
                objects[0], objects[4] = objects[4], objects[0] 
                objects[1], objects[5] = objects[5], objects[1] 
                objects[2], objects[6] = objects[6], objects[2] 
                nextPage = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_DOWN:
                if i < 4:
                    i += 1
            elif event.key == pygame.K_UP:
                if i >= 0:
                    i -= 1 
            elif event.key == pygame.K_RETURN:
                objects[i].onclickFunction()
                if i == 1 and nextPage == False:
                    objects[0], objects[4] = objects[4], objects[0] 
                    objects[1], objects[5] = objects[5], objects[1] 
                    objects[2], objects[6] = objects[6], objects[2] 
                    if nextPage == True:
                        nextPage = False
                    elif nextPage == False:
                        nextPage = True
                if i == 3:
                    nextPage = False
                    i = 1
                

    titleObjects[0].process()
    for object in objects[0:3]:
        object.process()
        if i == 0:
            objects[i].process(True)
        if i == 1:
            objects[i].process(True)
        if i == 2:
            objects[i].process(True)
        if nextPage == True:
            objects[3].process()
            if i == 3:
                objects[i].process(True)

            


    pygame.display.flip()
    fpsClock.tick(fps)

import pygame as pg
import pygame_gui as pg_gui
from Game import *

pg.init()

# 게임 창 크기 및 이름 설정
screenWidth = 800
screenHeight = 600
windowSize = (screenWidth, screenHeight)
screen=pg.display.set_mode(windowSize)
pg.display.set_caption("UNO GAME")

# ui 매니저
uiManager = pg_gui.UIManager(windowSize)
clock = pg.time.Clock()

# 색상 정의
DARKGREEN = (8, 44, 15)
GREY = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARKRED = (87, 4, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 127, 127)
BLACK = (0, 0, 0)

# 폰트 설정
font = pg.font.SysFont(None, 30)
unoFont = pg.font.SysFont(None, 40)

# 기본 배경 설정
backgroundColor = DARKGREEN
playerBgColor = GREY
myBgColor = DARKRED

# 타이머 설정
totalTime = 11
startTicks = pg.time.get_ticks()


# game start
def initGame(gamePlayers):

    computer = Player("COMPUTER")
    gamePlayers.append(computer)

    game = Game(gamePlayers)
    # print(game.players[0].cards[0].color)
    global DECK
    DECK = game.deck
    cardBackList = []
    cardBackImg = pg.image.load('unoCardBack.png').convert_alpha()
    cardBackRec = cardBackImg.get_rect()
    for i in range(len(DECK.cards)):
        cardBackRec.left = screenWidth*0.25-i/10
        cardBackRec.top = screenHeight*0.25-i/10
        cardBackList.append(cardBackRec)
        screen.blit(cardBackImg, cardBackRec)

    for i in range(len(game.players[1].cards)):
        cardBackList[i].left = screenWidth*0.92-i*20
        cardBackList[i].top = screenHeight*0.15
        playerCard = pg.transform.scale(cardBackImg, (cardBackRec.size[0]*0.6, cardBackRec.size[1]*0.6))
        screen.blit(playerCard, cardBackList[i])
    
    
    card_reacted = False

    for i in range(len(game.players[0].cards)):
        if i == 0:
            cardBackList[i].left = screenWidth*0.05
            cardBackList[i].top = screenHeight*0.80

        else:
            cardBackList[i].left = cardBackList[i-1].left + (screenWidth*0.05)

        mousePos = pg.mouse.get_pos()

        if not card_reacted and cardBackList[i].collidepoint(mousePos):
            print(i)
            cardBackList[i].top = screenHeight*0.75
            myCard = pg.transform.scale(cardBackImg, (cardBackRec.size[0], cardBackRec.size[1]))
            screen.blit(myCard, cardBackList[i])
            card_reacted = True 
        else:
            cardBackList[i].top = screenHeight*0.80
            myCard = pg.transform.scale(cardBackImg, (cardBackRec.size[0], cardBackRec.size[1]))
            screen.blit(myCard, cardBackList[i])    
        


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def timer(setTimer):
    global startTicks, totalTime
    if setTimer == True:
        elapsedTime = (pg.time.get_ticks()-startTicks)/1000
        if totalTime - elapsedTime > 0:
            timer = font.render(str(int(totalTime - elapsedTime)), True, WHITE)
            screen.blit(timer, (20, 20))
        elif totalTime - elapsedTime > -1:
            timeout = font.render("TIME OUT", True, WHITE)
            screen.blit(timeout, (20, 20))
        else:
            setTimer = False
            return setTimer
    else:
        setTimer = False
        return setTimer

def drawGameScreen():
    # 배경 색 설정/추후 배경사진 추가
    screen.fill(backgroundColor)

    # 플레이어 스크린 우측에 배치
    playerBgRec = pg.Rect(screenWidth*0.75, 0, screenWidth*0.25, screenHeight)
    # 나의 스크린 하단에 배치 
    myBgRect = pg.Rect(0, screenHeight* 0.75, screenWidth*0.75, screenHeight*0.25)

    pg.draw.rect(screen, playerBgColor, playerBgRec)
    pg.draw.rect(screen, myBgColor, myBgRect)
    whoArePlayers = font.render("PLAYER", True, WHITE)
    playersRec = whoArePlayers.get_rect()
    playersRec.centerx = round(screenWidth*0.875)
    playersRec.y = 20
    screen.blit(whoArePlayers, playersRec)

    # UNO 버튼 삽입
    unoButtonImg = pg.image.load('unobutton.png').convert_alpha()
    unoButton = Button(screenWidth*0.55, screenHeight*0.45, unoButtonImg)
    unoButton.draw()

def startGamePage():
    running = True
    while running:
        dt = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            uiManager.process_events(event)

        drawGameScreen()

        # game start
        player1 = Player("PLAYER 1")
        gamePlayers = [player1]
        initGame(gamePlayers)   
            

        # 타이머 삽입
        timer(True)

        uiManager.update(dt)
        uiManager.draw_ui(screen)
        pg.display.update()


# pg.quit()
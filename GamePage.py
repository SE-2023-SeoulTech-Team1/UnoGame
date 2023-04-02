import pygame as pg
import pygame_gui as pg_gui
import sys
from Game import *
from animation import *

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
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 127, 127)
BLACK = (0, 0, 0)

SELECT_COLOR = {"red" : (175,10,29), "green" : (34,139,34), "blue" : (0,0,205), "yellow" : (255,255,0)}

color_rects = [
    pg.Rect(screenWidth * 0.05, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 60, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 120, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 180, screenHeight * 0.65, 50, 50)
]


# 폰트 설정
font = pg.font.SysFont(None, 30)
unoFont = pg.font.SysFont(None, 40)

# 기본 배경 설정
backgroundColor = DARKGREEN
playerBgColor = GREY


# 카드 이미지 불러오기
def cardFrontImg(color, type):
    return pg.image.load('./assets/cards/' + color + type + '.png').convert_alpha()


# 카드 앞면 출력
def draw_card_front(card, top, left):
    card_front_img = pg.image.load(card.front).convert_alpha()
    screen.blit(card_front_img, (left, top))


# 카드 뒷면 출력
def draw_card_back(card, top, left):
    card_back_img = pg.image.load(card.back).convert_alpha()
    screen.blit(card_back_img, (left, top))


# 덱 카드 그리기
def draw_deck(game):
    for i, card in enumerate(game.deck.cards):
        card_back_img = pg.image.load(card.back).convert_alpha()
        top = screenHeight * 0.25 - i / 10
        left = screenWidth * 0.25 - i / 10
        screen.blit(card_back_img, (left, top))
    deck_rec = pg.Rect(left, top, card_back_img.get_width(), card_back_img.get_height())
    return deck_rec


# 현재 player card를 hover_card에서 그리고 있어 필요없음
#def draw_player_cards(game):
#    player = game.players[0]
#    for i, card in enumerate(player.cards):
#        top = screenHeight * 0.80
#        left = screenWidth * 0.05 + i * 30
#        draw_card_front(card, top, left)


# 컴퓨터 카드 그리기
def draw_computer_cards(game):
    computer = game.players[1]
    for i, card in enumerate(computer.cards):
        card_back_img = pg.image.load(card.back).convert_alpha()
        card_rec = card_back_img.get_rect()
        card_back_img = pg.transform.scale(card_back_img, (card_rec.size[0] * 0.7, card_rec.size[1] * 0.7))
        top = screenHeight * 0.15
        left = screenWidth * 0.92 - i * 20
        screen.blit(card_back_img, (left, top))



def move_card(game, card, start, end):
    top = screenHeight * 0.25
    left = screenWidth * 0.4

    # 카드 목표 위치 도달까지 위치 변경
    if card_loc <= left:
        card_loc += 10
        draw_card_front(openned_cards[0], top, card_loc)
    else:
        draw_card_front(openned_cards[0], top, card_loc)
        # 덱에서 카드가 뒤집힌 후 첫 턴의 시작은 player0
        # game.current_player_index = 0
        if timerFlag == True:
            timer(timerFlag, 10, game)

# 덱 카드 한 장 뒤집기
def flip_deck_card(game, flip_card):
    global openned_cards, card_loc

    # game의 pick_current_card 사용해서 게임 시작 직후 current card 정보 불러오고 open된 카드 리스트에 저장
    if flip_card is True:
        openned_cards = []
        game.pick_current_card()
        openned_cards.append(game.current_card)
        print(f"\n현재 뒤집어진 카드는 {game.current_card} 입니다.")

        # 카드의 현재 위치 저장
        card_loc = screenWidth * 0.25
        flip_card = False

    # 오픈된 카드 목표 위치
    top = screenHeight * 0.25
    left = screenWidth * 0.4

    # 카드 목표 위치 도달까지 위치 변경
    if card_loc <= left:
        card_loc += 10
        draw_card_front(openned_cards[0], top, card_loc)
    else:
        draw_card_front(openned_cards[0], top, card_loc)
        # 덱에서 카드가 뒤집힌 후 첫 턴의 시작은 player0
        # game.current_player_index = 0
        if timerFlag == True:
            timer(timerFlag, 10, game)

# 덱에 있는 카드와 일치 유무 
def valid_play(card1, card2):

    if (card1.color) == 'black':
        return True
    if (card2.color) == 'black':
        return True
    return card1.color == card2.color or card1.type == card2.type

# 카드 명암 적용 
def apply_shadow(image, alpha=100, color=(0, 0, 0)):
    shadow_surface = pg.Surface(image.get_size(), pg.SRCALPHA)
    shadow_surface.fill((*color, alpha))
    result_image = image.copy()
    result_image.blit(shadow_surface, (0, 0))
    return result_image

def hover_card(game, selected_card):
    card_reacted = False
    cardFrontList = []
    
    for i, card in enumerate(game.players[0].cards):
        card_front_img = pg.image.load(card.front).convert_alpha()
        card_rect = card_front_img.get_rect()
        if i == 0:
            card_rect.left = screenWidth * 0.05
            card_rect.top = screenHeight * 0.80
        else:
            card_rect.left = cardFrontList[i - 1].left + (screenWidth * 0.05)
            card_rect.top = screenHeight * 0.80

        cardFrontList.append(card_rect)
        mousePos = pg.mouse.get_pos()


        if not card_reacted and cardFrontList[i].collidepoint(mousePos):
            cardFrontList[i].top = screenHeight * 0.75
            darkened_image = apply_shadow(card_front_img)
            screen.blit(darkened_image, cardFrontList[i])
            card_reacted = True

            if valid_play(game.players[0].cards[i], openned_cards[0]):
                screen.blit(card_front_img,cardFrontList[i])

            color_selected = False

            # hover된 카드 Rect 클릭했을 때     
            if selected_card is not None and cardFrontList[i].collidepoint(selected_card):
                if game.players[0].cards[i].type == 'wildcard':
                    print("selected!!")
                    wildcard_selected = True

                    pg.draw.rect(screen, SELECT_COLOR['red'], color_rects[0])
                    pg.draw.rect(screen, SELECT_COLOR['blue'], color_rects[1])
                    pg.draw.rect(screen, SELECT_COLOR['yellow'], color_rects[2])
                    pg.draw.rect(screen, SELECT_COLOR['green'], color_rects[3])
                    
                    # i+1번째 부터 카드 추가 해야 됨 
                    for j in range(i+1, len(game.players[0].cards)):
                        card_rect.left = cardFrontList[j - 1].left + (screenWidth * 0.05)
                        card_rect.top = screenHeight * 0.80
                        cardFrontList.append(card_rect)
                        cardFrontList[j].top = screenHeight * 0.80
                        screen.blit(pg.image.load(game.players[0].cards[j].front).convert_alpha(), cardFrontList[j])

                    pg.display.flip()

                    # 플레이어가 색깔 고를 때 까지 기다림 
                    while not color_selected:
                                
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                                sys.exit()

                            if event.type == pg.MOUSEBUTTONDOWN:
                                mouse_pos = pg.mouse.get_pos()
                                for idx, color_rect in enumerate(color_rects):
                                    if color_rect.collidepoint(mouse_pos):
                                        color_selected = True
                                        print()
                                        break
                    
                    del cardFrontList[i+1 : len(game.players[0].cards)]

                if valid_play(game.players[0].cards[i], openned_cards[0]):
                    openned_cards.insert(0, game.players[0].cards[i])
                    game.players[0].cards.pop(i)
                    selected_card = None
                    break

        else:
            cardFrontList[i].top = screenHeight * 0.80
            screen.blit(card_front_img, cardFrontList[i])

    return selected_card

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class WarningMessage():
    def __init__(self, text):
        self.text = text
    def draw(self):
        pg.font.Font('freesansbold.ttf', 32)
        text = font.render(self.text, True, RED, None)
        text_rec = text.get_rect()
        text_rec.top = 100
        text_rec.left = screenWidth // 3
        screen.blit(text, text_rec)
        pg.display.update()
        time.sleep(1)

# 타이머 설정
timerFlag = True
count = True

# 타이머 정의
def timer(setTimer, totalTime, game):
    global timerFlag, startTicks, count

    # timer 최초 호출
    if count is True:
        startTicks = pg.time.get_ticks()
        print(f"\n현재 {game.players[game.current_player_index].name}의 턴입니다.")
        count = False

    # timer 실행
    if setTimer == True:
        elapsedTime = (pg.time.get_ticks()-startTicks) / 1000
        if totalTime - elapsedTime > 0:
            elapsedTime = (pg.time.get_ticks()-startTicks) / 1000
            timer = font.render(str(int(totalTime - elapsedTime)), True, WHITE)
            screen.blit(timer, (20, 20))
        elif totalTime - elapsedTime > -1:
            timeout = font.render("TIME OUT", True, WHITE)
            screen.blit(timeout, (20, 20))
        else:
            setTimer = False
            timerFlag = False
            count = True
            print("\n제한시간이 지났습니다. 상대 턴입니다.")
            # 다음 플레이어로 넘어가기 -> game 함수 메서드로 고치면 수정
            game.current_player_index = (game.current_player_index + game.direction) % len(game.players)
            # 타이머 종료 후 넘어간 턴 확인
            #print(f"\n현재 {game.players[game.current_player_index].name}의 턴입니다.")


def drawGameScreen():
    # 배경 색 설정/추후 배경사진 추가
    screen.fill(backgroundColor)

    # 플레이어 스크린 우측에 배치
    playerBgRec = pg.Rect(screenWidth*0.75, 0, screenWidth*0.25, screenHeight)
    pg.draw.rect(screen, playerBgColor, playerBgRec)

    whoArePlayers = font.render("PLAYER", True, WHITE)
    playersRec = whoArePlayers.get_rect()
    playersRec.centerx = round(screenWidth*0.875)
    playersRec.y = 20
    screen.blit(whoArePlayers, playersRec)

    # UNO 버튼 삽입
    unoButtonImg = pg.image.load('./assets/unobutton.png').convert_alpha()
    unoButton = Button(screenWidth*0.55, screenHeight*0.45, unoButtonImg)
    unoButton.draw()


def process_deck_clicked(game):
    popped_card = game.deck.pop_card()
    game.players[0].cards.append(popped_card)


def startGamePage():

    game = Game([Player("PLAYER0"), Computer(0)])
    # 카드 초기 세팅 
    game.deal_cards()

    # players[0] 카드 출력
    print(f"\n{game.players[0].name}'s cards:")
    for i in range(len(game.players[0].cards)):
        print(game.players[0].cards[i])

    selected_card = None
    flip_card = True
    running = True

    drawGameScreen()
    deck_rec = draw_deck(game)
    draw_computer_cards(game)
    flip_card = flip_deck_card(game, flip_card)

    while running:

        dt = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                selected_card = event.pos
                if deck_rec.collidepoint(event.pos):
                    if game.current_player_index == 0:
                        process_deck_clicked(game)
                        game.current_player_index = 1
                    else:
                        WarningMessage("It's not your turn!").draw()


            uiManager.process_events(event)

        drawGameScreen()
        deck_rec = draw_deck(game)
        flip_card = flip_deck_card(game, flip_card)
        draw_computer_cards(game)

        if game.current_player_index != 0:
            if game.players[game.current_player_index].can_play(game.current_card):
                popped_card = game.players[game.current_player_index].play_card(game)
                card_front_img = pg.image.load(popped_card.front).convert_alpha().get_rect()
                openned_cards.insert(0, popped_card)
                # animate_rect(screen, card_front_img, (100, 100), (500, 300), 2000)
            else:
                game.players[game.current_player_index].draw_card(game.deck)
            game.current_player_index = 0

        selected_card = hover_card(game, selected_card)

        uiManager.update(dt)
        uiManager.draw_ui(screen)
        pg.display.update()
import pygame as pg
import pygame_gui as pg_gui
import sys
from Game import *
from FunctionAnimation import *
from random import randint
from animation import *

pg.init()

# ui 매니저
uiManager = pg_gui.UIManager(windowSize)
clock = pg.time.Clock()

color_rects = [
    pg.Rect(screenWidth * 0.05, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 60, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 120, screenHeight * 0.65, 50, 50),
    pg.Rect(screenWidth * 0.05 + 180, screenHeight * 0.65, 50, 50)
]


# 덱 카드 그리기
def draw_deck(game):
    for i, card in enumerate(game.deck.cards):
        card_back_img = pg.image.load(card.back).convert_alpha()
        top = screenHeight * 0.25 - i / 10
        left = screenWidth * 0.25 - i / 10
        screen.blit(card_back_img, (left, top))
    deck_rec = pg.Rect(left, top, card_back_img.get_width(),
                    card_back_img.get_height())
    return deck_rec


# 컴퓨터 카드 그리기
def draw_computer_cards(game):
    computer_card_rect_list = []
    computer = game.players[1]
    for i, card in enumerate(computer.cards):
        card_back_img = pg.image.load(card.back).convert_alpha()
        card_rec = card_back_img.get_rect()
        card_back_img = pg.transform.scale(
            card_back_img, (card_rec.size[0] * 0.7, card_rec.size[1] * 0.7))
        card_rec.top = screenHeight * 0.15
        card_rec.left = screenWidth * 0.92 - i * 20
        computer_card_rect_list.append(card_rec)
        screen.blit(card_back_img, card_rec)
    return computer_card_rect_list



# 덱 카드 한 장 뒤집기
def flip_deck_card(game, flip_card):
    global openned_cards, card_loc, timerFlag

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
        draw_card_front(screen, openned_cards[0], top, card_loc)
    else:
        draw_card_front(screen, openned_cards[0], top, card_loc)

        if timerFlag == True:
            timer(timerFlag, TIMEOUT, game)
        timerFlag = True


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


# black카드 일 때
def handle_black(game, card_rect, i, chosen_card, screen, cardFrontList, screenWidth, screenHeight):

    pg.draw.rect(screen, SELECT_COLOR['red'], color_rects[0])
    pg.draw.rect(screen, SELECT_COLOR['green'], color_rects[1])
    pg.draw.rect(screen, SELECT_COLOR['blue'], color_rects[2])
    pg.draw.rect(screen, SELECT_COLOR['yellow'], color_rects[3])

    # i+1번째 부터 카드 추가 해야 됨
    for j in range(i+1, len(game.players[0].cards)):
        card_rect.left = cardFrontList[j - 1].left + (screenWidth * 0.05)
        card_rect.top = screenHeight * 0.80
        cardFrontList.append(card_rect)
        cardFrontList[j].top = screenHeight * 0.80
        screen.blit(pg.image.load(
            game.players[0].cards[j].front).convert_alpha(), cardFrontList[j])

    pg.display.flip()

    # 플레이어가 색깔 고를 때 까지 기다림
    color_selected = False
    while not color_selected:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                for idx, color_rect in enumerate(color_rects):
                    if color_rect.collidepoint(mouse_pos):
                        chosen_color = list(SELECT_COLOR.keys())[idx]
                        if chosen_card.type == 'wildcard':
                            game.wildcard_card_clicked(chosen_color)
                        elif chosen_card.type == '+4':
                            end_pos = draw_computer_cards(game)[-1]
                            for i in range(4):
                                added_card = game.deck.cards[-(i+1)]
                                added_card_img = pg.image.load(added_card.back).convert_alpha()
                                added_card_rect = added_card_img.get_rect()
                                start_pos = draw_deck(game)
                                end_pos.x = end_pos.x - 20
                                move_card_animation(game, added_card_img, added_card_rect, 
                                                    (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                                screen.blit(added_card_img, (end_pos.x, end_pos.y))
                            game.plus4_card_clicked(game.players[0], chosen_color)
                        color_selected = True
                        break

    del cardFrontList[i+1: len(game.players[0].cards)]


def redraw_card(game, i, screen, card_rect, card_rect_list):
    for j in range(i+1, len(game.players[0].cards)):
        card_rect.left = card_rect_list[j - 1].left + (screenWidth * 0.05)
        card_rect.top = screenHeight * 0.80
        card_rect_list.append(card_rect)
        card_rect_list[j].top = screenHeight * 0.80
        screen.blit(pg.image.load(
            game.players[0].cards[j].front).convert_alpha(), card_rect_list[j])


def handle_card_hover(game, screen, card_rect_list, screenHeight):
    mouse_pos = pg.mouse.get_pos()

    card_reacted = False
    for i, card_rect in enumerate(card_rect_list):

        if i >= len(game.players[0].cards):
            continue  # 유효하지 않은 인덱스를 건너뛰기
        card_front_img = pg.image.load(game.players[0].cards[i].front).convert_alpha()

        if not card_reacted and card_rect.collidepoint(mouse_pos):
            card_rect.top = screenHeight * 0.75
            darkened_image = apply_shadow(card_front_img)
            screen.blit(darkened_image, card_rect)
            card_reacted = True

            if valid_play(game.players[0].cards[i], openned_cards[0]):
                screen.blit(card_front_img, card_rect)

                # 카드 클릭 로직 
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN:
                        openned_cards.insert(0, game.players[0].cards[i])
                        game.current_card = openned_cards[0]

                        chosen_card = game.players[0].cards[i]
                        game.players[0].cards.pop(i)
                        chosen_card_img = pg.image.load(chosen_card.front).convert_alpha()
                        chosen_card_rect = card_rect_list[i]
                        start_pos = card_rect_list[i]
                        move_card_animation(game, chosen_card_img, chosen_card_rect, 
                                            (start_pos.x, start_pos.y), (screenWidth*0.4, screenHeight*0.25))
                            

                        # 기능 카드 눌렀을 때 
                        if game.current_card.type == 'wildcard':
                            handle_black(game, card_rect, i, chosen_card, screen, card_rect_list, screenWidth, screenHeight)
                        elif game.current_card.type == '+4':
                            handle_black(game, card_rect, i, chosen_card, screen, card_rect_list, screenWidth, screenHeight)
                        elif game.current_card.type == '+2':
                            end_pos = draw_computer_cards(game)[-1]
                            for i in range(2):
                                added_card = game.deck.cards[-(i+1)]
                                added_card_img = pg.image.load(added_card.back).convert_alpha()
                                added_card_rect = added_card_img.get_rect()
                                start_pos = draw_deck(game)
                                end_pos.x = end_pos.x - 20
                                move_card_animation(game, added_card_img, added_card_rect, 
                                                    (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                                screen.blit(added_card_img, (end_pos.x, end_pos.y))
                            game.plus2_card_clicked(game.players[0])
                        elif game.current_card.type == 'reverse':
                            # 클릭했을 때 오른쪽 카드 이미지들 누락 방지를 위한 코드 
                            redraw_card(game, i, screen, card_rect, card_rect_list)

                            if game.direction == 1:
                                reverse_icon = pg.image.load("./assets/counterclockwise.png")
                                reverse_icon = pg.transform.scale(reverse_icon, (150, 150))
                            elif game.direction == -1:
                                reverse_icon = pg.image.load("./assets/clockwise.png")
                                reverse_icon = pg.transform.scale(reverse_icon, (150, 150))

                            display_reverse_animation(screen, reverse_icon)

                            game.reverse_card_clicked()

                            # 다시 오른쪽카드들 그려지므로 삭제 
                            del card_rect_list[i+1: len(game.players[0].cards)]

                        elif game.current_card.type == 'skip':
                            redraw_card(game, i, screen, card_rect, card_rect_list)

                            game.skip_card_clicked()
                            # 로직은 나중에 functionCard 기능 고쳐지면 그 때 수정 --> 지금은 일시적으로 
                            display_skip_animation(screen, game.players[game.current_player_index + 1].name)

                            del card_rect_list[i+1: len(game.players[0].cards)]
                            game.players[0].cards.pop(i)

                        # game.players[0].cards.pop(i)
                        print(f"\n현재 뒤집어진 카드는 {game.current_card} 입니다.")
                        

        else:
            card_rect.top = screenHeight * 0.80
            screen.blit(card_front_img, card_rect)


def display_player_cards(game):
    card_rect_list = []

    for i, card in enumerate(game.players[0].cards):
        card_front_img = pg.image.load(card.front).convert_alpha()
        card_rect = card_front_img.get_rect()
        if i == 0:
            card_rect.left = screenWidth * 0.05
            card_rect.top = screenHeight * 0.80
        else:
            card_rect.left = card_rect_list[i - 1].left + (screenWidth * 0.05)
            card_rect.top = screenHeight * 0.80

        card_rect_list.append(card_rect)

    handle_card_hover(game, screen, card_rect_list, screenHeight)
    return card_rect_list

class Message():
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = color

    def draw(self):
        pg.font.Font('freesansbold.ttf', self.size)
        text = font.render(self.text, True, self.color, None)
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
    global timerFlag, startTicks, count, deck_cards_num, player_cards_num

    # timer 최초 호출
    if count is True:
        startTicks = pg.time.get_ticks()
        print(f"\n현재 {game.players[game.current_player_index].name}의 턴입니다.")
        deck_cards_num = len(game.deck.cards)
        player_cards_num = len(game.players[0].cards)
        count = False

    # timer 실행
    if setTimer == True:
        elapsed_time = (pg.time.get_ticks()-startTicks) / 1000
        if totalTime - elapsed_time > 0 and deck_cards_num == len(game.deck.cards) and player_cards_num == len(game.players[0].cards):
            elapsed_time = (pg.time.get_ticks()-startTicks) / 1000
            timer = font.render(str(int(totalTime - elapsed_time)), True, WHITE)
            screen.blit(timer, (20, 20))
            who_is_current_player(game)
        elif deck_cards_num != len(game.deck.cards) or player_cards_num != len(game.players[0].cards):
            setTimer = False
            timerFlag = False
            count = True
            game.next_turn()
        elif totalTime - elapsed_time > -1:
            timeout = font.render("TIME OUT", True, WHITE)
            screen.blit(timeout, (20, 20))
            who_is_current_player(game)
        else:
            setTimer = False
            timerFlag = False
            count = True
            print("\n제한시간이 지났습니다. 상대 턴입니다.")
            # 다음 플레이어로 넘어가기
            game.next_turn()

def current_card_color(game):
    card_color = game.current_card.color
    current_card_rect = pg.Rect(playerBgx - 60, playerBgy + 20, 40, 40)
    if card_color == 'red':
        pg.draw.rect(screen, RED, current_card_rect)
    elif card_color == 'blue':
        pg.draw.rect(screen, BLUE, current_card_rect)
    elif card_color == 'green':
        pg.draw.rect(screen, GREEN, current_card_rect)
    elif card_color == 'yellow':
        pg.draw.rect(screen, YELLOW, current_card_rect)

def who_is_current_player(game):
    player = font.render(game.players[game.current_player_index].name, True, WHITE)
    player_rect = player.get_rect()
    player_rect.centerx = round(boardx + boardWidth*0.5)
    player_rect.y = 20
    screen.blit(player, player_rect)


def unobutton(game):
    unobutton_img = pg.image.load('./assets/unobutton.png').convert_alpha()
    unobutton_rect = unobutton_img.get_rect()
    unobutton_rect.centerx = round(boardx + boardWidth*0.5)
    unobutton_rect.y = screenHeight * 0.45
    screen.blit(unobutton_img, unobutton_rect)
    return unobutton_rect


def move_card_animation(game, card_img, card_rect, start_pos, end_pos, duration=500):
    start_time = pg.time.get_ticks()
    elapsed_time = 0
    distance = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    while elapsed_time < duration:
        elapsed_time = pg.time.get_ticks() - start_time
        progress = min(elapsed_time / duration, 10)
        new_pos = start_pos[0] + distance[0] * progress, start_pos[1] + distance[1] * progress
        card_rect.x, card_rect.y = new_pos
        screen.blit(card_img, (card_rect.left, card_rect.top))
        pg.display.flip()
        drawGameScreen(screen, game)
        unobutton(game)
        draw_deck(game)
        draw_card_front(screen, openned_cards[0], screenHeight * 0.25, card_loc)
        current_card_color(game)
        who_is_current_player(game)
        draw_computer_cards(game)
        display_player_cards(game)


# duration 동안 계속 screen.blit
# def move_card_animation(game, card, start_pos, end_pos, duration=500):
#     start_time = pg.time.get_ticks()
#     elapsed_time = 0
#     distance = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

#     card_img = pg.image.load(card.front).convert_alpha()
#     card_rect = card_img.get_rect()

#     while elapsed_time < duration:
#         elapsed_time = pg.time.get_ticks() - start_time
#         progress = min(elapsed_time / duration, 10)
#         new_pos = start_pos[0] + distance[0] * progress, start_pos[1] + distance[1] * progress
#         card_rect.x, card_rect.y = new_pos
#         screen.blit(card_img, (card_rect.left, card_rect.top))
#         pg.display.flip()


def process_deck_clicked(game, deck_rect, end_pos):
    popped_card = game.deck.pop_card()
    end_pos.x = end_pos.x + (screenWidth * 0.05)
    card_img = pg.image.load(popped_card.front).convert_alpha()
    card_rect = card_img.get_rect()

    move_card_animation(game, card_img, card_rect, (deck_rect.x, deck_rect.y), (end_pos.x, end_pos.y))
    game.players[0].cards.append(popped_card)
    print(f"\n{game.players[game.current_player_index].name}이 deck에서 카드를 한 장 받습니다.")
    


# 컴퓨터가 기능 카드 낼 때 
def computer_function_card(game):
    if game.current_card.color == 'black':
        choiced_color = game.players[game.current_player_index].black_card_clicked()
        if game.current_card.type == 'wildcard':
            game.wildcard_card_clicked(choiced_color)
        elif game.current_card.type == '+4':
            end_pos = display_player_cards(game)[-1]
            for i in range(4):
                added_card = game.deck.cards[-(i+1)]
                added_card_img = pg.image.load(added_card.front).convert_alpha()
                added_card_rect = added_card_img.get_rect()
                start_pos = draw_deck(game)
                end_pos.x = end_pos.x + (screenWidth * 0.05)
                move_card_animation(game, added_card_img, added_card_rect, 
                                    (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                screen.blit(added_card_img, (end_pos.x, end_pos.y))
            game.plus4_card_clicked(game.players[game.current_player_index], choiced_color)
    elif game.current_card.type == '+2':
        end_pos = display_player_cards(game)[-1]
        for i in range(2):
            added_card = game.deck.cards[-(i+1)]
            added_card_img = pg.image.load(added_card.front).convert_alpha()
            added_card_rect = added_card_img.get_rect()
            start_pos = draw_deck(game)
            end_pos.x = end_pos.x + (screenWidth * 0.05)
            move_card_animation(game, added_card_img, added_card_rect, 
                                (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
            screen.blit(added_card_img, (end_pos.x, end_pos.y))
        game.plus2_card_clicked(game.players[game.current_player_index])
    elif game.current_card.type == 'reverse':
        if game.direction == 1:
            reverse_icon = pg.image.load("./assets/counterclockwise.png")
            reverse_icon = pg.transform.scale(reverse_icon, (200, 200))
        else:
            reverse_icon = pg.image.load("./assets/clockwise.png")
            reverse_icon = pg.transform.scale(reverse_icon, (200, 200))
        display_reverse_animation(screen, reverse_icon)
        game.reverse_card_clicked()


    elif game.current_card.type == 'skip':
        game.skip_card_clicked()
        # 게임 function card 버그 고쳐지면 수정 --> 지금은 애니메이션만 일시적으로 해놓음 
        display_skip_animation(screen, game.players[game.current_player_index - 1].name)



def startGamePage():

    game = Game([Player("PLAYER0"), Computer("computer0")], True)
    # 카드 초기 세팅
    game.deal_cards()

    # players[0] 카드 출력
    print(f"\n{game.players[0].name}'s cards:")
    for i in range(len(game.players[0].cards)):
        print(game.players[0].cards[i])

    flip_card = True
    running = True

    drawGameScreen(screen, game)
    deck_rect = draw_deck(game)
    draw_computer_cards(game)
    flip_card = flip_deck_card(game, flip_card)
    unobutton_rect = unobutton(game)
    card_rect_list = display_player_cards(game)

    while running:
        
        dt = clock.tick(60)/1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if deck_rect.collidepoint(event.pos):
                    if game.current_player_index == 0:
                        process_deck_clicked(game, deck_rect, card_rect_list[-1])
                    else:
                        Message("It's not your turn!", 32, RED).draw()
                if unobutton_rect.collidepoint(event.pos):
                    print("UNO button clicked - user")
                    if game.uno_button_clicked(0):
                        Message("UNO", 100, BLUE).draw()
                    else:
                        Message("WRONG UNO", 100, RED).draw()


            uiManager.process_events(event)

        drawGameScreen(screen, game)
        unobutton(game)
        deck_rect = draw_deck(game)
        current_card_color(game)
        flip_card = flip_deck_card(game, flip_card)
        draw_computer_cards(game)
        card_rect_list = display_player_cards(game)
        computer_card_rect_list = draw_computer_cards(game)

        player_with_one_card = [player for player in game.players if len(player.cards) == 1]
        player_with_no_card = [player for player in game.players if len(player.cards) == 0]
        if player_with_one_card:
            if randint(0, 1):
                game.uno_button_clicked(1)
                Message("UNO", 100, BLUE).draw()
                print("UNO button clicked - computer")

        elif player_with_no_card:
            Message(f"PLAYER{player_with_no_card} WIN")
            exit(0)

        if game.current_player_index != 0:
            if game.players[game.current_player_index].can_play(game.current_card):
                print(f"\n현재 {game.players[game.current_player_index].name}의 턴입니다.")
                # 현재 플레이어 화면 출력
                who_is_current_player(game)
                pg.display.update()

                card_idx_can_play = game.players[game.current_player_index].can_play(game.current_card)
                popped_card = game.players[game.current_player_index].play_card(game)
                card_idx_after_can_play = game.players[game.current_player_index].can_play(game.current_card)

                card_idx = [x for x in card_idx_can_play if x not in card_idx_after_can_play]
                idx = card_idx[0]
                popped_card_back_img = pg.image.load(popped_card.back).convert_alpha()
                popped_card_rect = computer_card_rect_list[idx]

                openned_cards.insert(0, popped_card)

                # current card 업데이트
                game.current_card = openned_cards[0]
                # function card 일 때 
                computer_function_card(game)

                start_pos = popped_card_rect
                move_card_animation(game, popped_card_back_img, popped_card_rect, 
                                    (start_pos.x, start_pos.y), (screenWidth*0.4, screenHeight*0.25))
                
                print(f"\n현재 뒤집어진 카드는 {game.current_card} 입니다.")
                # animate_rect(screen, card_front_img, (100, 100), (500, 300), 2000)
            else:
                print(f"\n현재 {game.players[game.current_player_index].name}의 턴입니다.")
                # 현재 플레이어 화면 출력
                who_is_current_player(game)
                pg.display.update()

                print(f"\n{game.players[game.current_player_index].name}이 deck에서 카드를 한 장 받습니다.")
                game.players[game.current_player_index].draw_card(game.deck)
                new_computer_card = game.players[game.current_player_index].cards[-1]
                new_computer_card_img = pg.image.load(new_computer_card.back).convert_alpha()
                new_computer_card_rect = new_computer_card_img.get_rect()
                end_pos = computer_card_rect_list[-1]
                end_pos.x = end_pos.x - 20
                move_card_animation(game, new_computer_card_img, new_computer_card_rect, 
                                    (deck_rect.x, deck_rect.y), (end_pos.x, end_pos.y))
            game.current_player_index = 0

        uiManager.update(dt)
        uiManager.draw_ui(screen)
        pg.display.update()
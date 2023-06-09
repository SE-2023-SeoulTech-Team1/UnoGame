import pygame as pygame
import pygame_gui as pygame_gui
import sys
from Game import *
from StoryGame import *
from Achievement import *
from FunctionAnimation import *
from random import randint, shuffle
from draw import *
from Message import Message
from Text import Text
from UnoButton import UnoButton
from PausedPage import *
from resource_path import *
import pickle
import os
from threading import Event, Timer
from Test.storymode_test import test_deal_cards


class GamePage():
    def __init__(self, screen, setting, player_names=None, story_mode=None, achievement_page = None):
        self.setting = setting
        self.player_names = player_names
        self.achievement_page = achievement_page
        if story_mode is None:
            self.game = Game(self.player_names, self.setting.color_weak)
        elif story_mode == "A":
            self.player_names = ["Player", "Alien"]
            self.game = StoryGameA(self.setting.color_weak)
        elif story_mode == "B":
            self.player_names = ["Player", "Alien"]
            self.game = StoryGameB(self.setting.color_weak)
        elif story_mode == "C":
            self.player_names = ["Player", "Alien1", "Alien2", "Alien3"]
            self.game = StoryGameC(self.setting.color_weak)
        else:
            self.player_names = ["Player", "Alien1", "Alien2"]
            self.game = StoryGameD(self.setting.color_weak)
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.computer_players_names = [
            Text(text=name, x=0.8, y=0.16 * (i + 1) - 0.03, size=24, color=WHITE)
            for i, name in enumerate(self.player_names[1:])
        ]
        # card_rec.top = self.screen_height * 0.17 * (computer_player_idx + 1)
        self.uno_button = UnoButton(self)
        self.uno_button_pressed = False
        self.pause_page = PausedPage(self.screen, self.setting)

        self.card_move_sound = pygame.mixer.Sound(
            resource_path('./assets/cardmove.mp3'))
        self.card_select_sound = pygame.mixer.Sound(
            resource_path('./assets/cardclick.mp3'))

        self.color_rects = [
            pygame.Rect(self.screen_width * 0.05,
                        self.screen_height * 0.65, 50, 50),
            pygame.Rect(self.screen_width * 0.05 + 60,
                        self.screen_height * 0.65, 50, 50),
            pygame.Rect(self.screen_width * 0.05 + 120,
                        self.screen_height * 0.65, 50, 50),
            pygame.Rect(self.screen_width * 0.05 + 180,
                        self.screen_height * 0.65, 50, 50)
        ]

        self.timerFlag = True
        self.count = True
        self.uiManager = pygame_gui.UIManager(setting.screen_size)
        self.clock = pygame.time.Clock()
        self.key_idx = 0
        self.deck_rect = None
        self.openned_cards = []
        self.achievements = None


    def timer(self, setTimer, totalTime):
        global timerFlag, startTicks, count, deck_cards_num, player_cards_num

        # timer 최초 호출
        if self.count is True:
            startTicks = pygame.time.get_ticks()
            print(
                f"\n현재 {self.game.players[self.game.current_player_index].name}의 턴입니다.")
            deck_cards_num = len(self.game.deck.cards)
            player_cards_num = len(self.game.players[0].cards)
            self.count = False

        # timer 실행
        if setTimer == True:
            elapsed_time = (pygame.time.get_ticks()-startTicks) / 1000
            if totalTime - elapsed_time > 0 and deck_cards_num == len(self.game.deck.cards) and player_cards_num == len(self.game.players[0].cards):
                elapsed_time = (pygame.time.get_ticks()-startTicks) / 1000
                timer = font.render(
                    str(int(totalTime - elapsed_time)), True, WHITE)
                self.screen.blit(timer, (20, 20))
                self.who_is_current_player()
            elif deck_cards_num != len(self.game.deck.cards) or player_cards_num != len(self.game.players[0].cards):
                setTimer = False
                timerFlag = False
                self.count = True

                # 여기서 next_turn 안하고 카드들 선택한다음 그곳에서 next_turn하는 방식으로 바꿈
                # game.next_turn()
            elif totalTime - elapsed_time > -1:
                timeout = font.render("TIME OUT", True, WHITE)
                self.screen.blit(timeout, (20, 20))
                self.who_is_current_player()
            else:
                setTimer = False
                timerFlag = False
                self.count = True
                print("\n제한시간이 지났습니다. 상대 턴입니다.")
                # 다음 플레이어로 넘어가기
                self.game.next_turn()

    # 덱 카드 그리기
    def draw_deck(self):
        for i, card in enumerate(self.game.deck.cards):
            card_back_img = pygame.image.load(card.back).convert_alpha()
            top = self.screen_height * 0.25 - i / 10
            left = self.screen_width * 0.25 - i / 10
            self.screen.blit(card_back_img, (left, top))
        if len(self.game.deck.cards) > 0:
            deck_rec = pygame.Rect(left, top, card_back_img.get_width(),
                                   card_back_img.get_height())
            return deck_rec

    # 컴퓨터 카드 그리기
    def draw_computer_cards(self):
        computer_card_rect_list = []
        computer_players = self.game.players[1:]
        for computer_player_idx, computer_player in enumerate(computer_players):
            rect_list = []
            for card_idx, card in enumerate(computer_player.cards):
                card_back_img = pygame.image.load(card.back).convert_alpha()
                card_rec = card_back_img.get_rect()
                card_back_img = pygame.transform.scale(
                    card_back_img, (card_rec.size[0] * 0.7, card_rec.size[1] * 0.7))
                card_rec.top = self.screen_height * 0.17 * (computer_player_idx + 1)
                card_rec.left = self.screen_width * 0.92 - card_idx * 20
                rect_list.append(card_rec) 
                self.screen.blit(card_back_img, card_rec)
            computer_card_rect_list.append(rect_list)

        return computer_card_rect_list

    # 덱 카드 한 장 뒤집기
    def flip_deck_card(self, flip_card):
        global card_loc, timerFlag

        # game의 pick_current_card 사용해서 게임 시작 직후 current card 정보 불러오고 open된 카드 리스트에 저장
        if flip_card is True:
            if os.path.exists(resource_path('game_state.pkl')):
                pass
            else:
                self.game.pick_current_card()
            self.openned_cards.append(self.game.current_card)
            self.card_move_sound.play()
            self.card_move_sound.set_volume(
                self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
            print(f"\n현재 뒤집어진 카드는 {self.game.current_card} 입니다.")

            # 카드의 현재 위치 저장
            card_loc = self.screen_width * 0.25
            flip_card = False

        # 오픈된 카드 목표 위치
        top = self.screen_height * 0.25
        left = self.screen_width * 0.4

        # 카드 목표 위치 도달까지 위치 변경
        if card_loc <= left:
            card_loc += 10
            draw_card_front(self.screen, self.openned_cards[-1], top, card_loc)
        else:
            draw_card_front(self.screen, self.openned_cards[-1], top, card_loc)

            if self.timerFlag == True:
                self.timer(self.timerFlag, TIMEOUT)
            self.timerFlag = True

    # 덱에 있는 카드와 일치 유무
    def valid_play(self, card1, card2):

        if (card1.color) == 'black':
            return True
        if (card2.color) == 'black':
            return True
        return card1.color == card2.color or card1.type == card2.type

    # 카드 명암 적용
    def apply_shadow(self, image, alpha=100, color=(0, 0, 0)):
        shadow_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        shadow_surface.fill((*color, alpha))
        result_image = image.copy()
        result_image.blit(shadow_surface, (0, 0))
        return result_image

    # black카드 일 때
    def handle_black(self, card_rect, i, chosen_card, screen, cardFrontList, screen_width, screen_height):

        if self.game.color_weak_mode == True:
            idx = 0
        else:
            idx = 1

        pygame.draw.rect(self.screen, RED if idx ==
                         1 else W_RED, self.color_rects[0])
        pygame.draw.rect(self.screen, GREEN if idx ==
                         1 else W_GREEN, self.color_rects[1])
        pygame.draw.rect(self.screen, BLUE if idx ==
                         1 else W_BLUE, self.color_rects[2])
        pygame.draw.rect(self.screen, YELLOW if idx ==
                         1 else W_YELLOW, self.color_rects[3])

        # i+1번째 부터 카드 추가 해야 됨
        for j in range(i+1, len(self.game.players[0].cards)):
            card_rect.left = cardFrontList[j -
                                           1].left + (self.screen_width * 0.05)
            card_rect.top = self.screen_height * 0.80
            cardFrontList.append(card_rect)
            cardFrontList[j].top = self.screen_height * 0.80
            self.screen.blit(pygame.image.load(
                self.game.players[0].cards[j].front).convert_alpha(), cardFrontList[j])

        pygame.display.flip()

        # 플레이어가 색깔 고를 때 까지 기다림
        color_selected = False
        while not color_selected:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.card_select_sound.play()
                    self.card_select_sound.set_volume(
                        self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                    mouse_pos = pygame.mouse.get_pos()
                    for idx, color_rect in enumerate(self.color_rects):
                        if color_rect.collidepoint(mouse_pos):
                            chosen_color = list(SELECT_COLOR.keys())[idx]
                            if chosen_card.type == 'wildcard' and self.game.deck.len_card() >= 1:
                                self.game.wildcard_card_clicked(chosen_color)
                            elif chosen_card.type == '+4' and self.game.deck.len_card() >= 4:
                                if self.game.direction == 1:
                                    end_pos = self.draw_computer_cards()[self.game.current_player_index][-1]
                                else:
                                    # -2 이유 : draw_computer_cards의 첫번째 컴퓨터 idx == 0 임 -> - 1
                                    #          거기에 player_names 인덱스 이므로 -> - 1
                                    next_index = len(self.game.player_names) - 2
                                    end_pos = self.draw_computer_cards()[next_index][-1]

                                for i in range(4):
                                    added_card = self.game.deck.cards[-(i+1)]
                                    added_card_img = pygame.image.load(
                                        added_card.back).convert_alpha()
                                    added_card_rect = added_card_img.get_rect()
                                    start_pos = self.draw_deck()
                                    end_pos.x = end_pos.x - 20
                                    self.card_move_sound.play()
                                    self.card_move_sound.set_volume(
                                        self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                                    self.move_card_animation(added_card_img, added_card_rect,(start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                                    self.draw_computer_cards()[self.game.current_player_index]
                                    pygame.display.flip()
                                self.game.plus4_card_clicked(chosen_color)
                            elif chosen_card.type == 'bomb' and self.game.deck.len_card() >= (3 * (len(self.game.players)-1)):
                                # bomb 그림
                                bomb_icon = pygame.image.load(
                                    resource_path("./assets/bomb.png"))
                                bomb_icon = pygame.transform.scale(
                                    bomb_icon, (250, 250))
                                display_bomb_animation(self.screen, bomb_icon)

                                for i in range(len(self.game.players) - 1):
                                    end_pos = self.draw_computer_cards()[i][-1]
                                    for j in range(3):
                                        added_card = self.game.deck.cards[-(j+1)]
                                        added_card_img = pygame.image.load(
                                            added_card.back).convert_alpha()
                                        added_card_rect = added_card_img.get_rect()
                                        start_pos = self.draw_deck()
                                        end_pos.x = end_pos.x - 20
                                        self.card_move_sound.play()
                                        self.card_move_sound.set_volume(
                                            self.setting.volume * self.setting.effect_volume * 0.01)
                                        self.move_card_animation(added_card_img, added_card_rect,
                                                                (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                                        # self.draw_computer_cards(
                                        # )[self.game.current_player_index]
                                        pygame.display.flip()
                                self.game.bombcard_card_clicked(chosen_color)

                            elif chosen_card.type == 'all' and self.game.deck.len_card() >= 1:
                                current_name = self.game.players[self.game.current_player_index].name
                                target_name = self.game.players[self.game.current_player_index + 1].name
                                all_change_icon = pygame.image.load(
                                    resource_path("./assets/all_change.png"))
                                all_change_icon = pygame.transform.scale(
                                    all_change_icon, (200, 200))
                                display_all_change_animation(
                                    self.screen, all_change_icon, current_name, target_name)
                                self.game.change_all_clicked(1, chosen_color)
                            else:
                                self.game.deck.cards = self.game_deck_used_all()
                            color_selected = True
                            break

        del cardFrontList[i+1: len(self.game.players[0].cards)]

    def redraw_card(self, i, screen, card_rect, card_rect_list):
        for j in range(i+1, len(self.game.players[0].cards)):
            card_rect.left = card_rect_list[j -
                                            1].left + (self.screen_width * 0.05)
            card_rect.top = self.screen_height * 0.80
            card_rect_list.append(card_rect)
            card_rect_list[j].top = self.screen_height * 0.80
            self.screen.blit(pygame.image.load(
                self.game.players[0].cards[j].front).convert_alpha(), card_rect_list[j])

    # 사운드
    def card_sound(self):
        self.card_move_sound.play()
        self.card_move_sound.set_volume(
            self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)

    # 기능 카드 눌렸을 때
    def func_card_clicked(self, i, card_rect, chosen_card, card_rect_list):
        self.game.skill_card_used = True
        if self.game.current_card.type == 'all':
            self.handle_black(card_rect, i, chosen_card, self.screen,
                              card_rect_list, self.screen_width, self.screen_height)
        elif self.game.current_card.type == 'wildcard':
            self.handle_black(card_rect, i, chosen_card, self.screen,
                              card_rect_list, self.screen_width, self.screen_height)
        elif self.game.current_card.type == '+4':
            self.handle_black(card_rect, i, chosen_card, self.screen,
                              card_rect_list, self.screen_width, self.screen_height)
        elif self.game.current_card.type == 'bomb':
            self.handle_black(card_rect, i, chosen_card, self.screen,
                              card_rect_list, self.screen_width, self.screen_height)
        elif self.game.current_card.type == '+2' and self.game.deck.len_card() >= 2:
            # 방향이 반대일 때 생각 
            if self.game.direction == 1:
                end_pos = self.draw_computer_cards()[self.game.current_player_index][-1]
            else:
                next_index = len(self.game.player_names) - 2
                end_pos = self.draw_computer_cards()[next_index][-1]
            for i in range(2):
                added_card = self.game.deck.cards[-(i+1)]
                added_card_img = pygame.image.load(
                    added_card.back).convert_alpha()
                added_card_rect = added_card_img.get_rect()
                start_pos = self.draw_deck()
                end_pos.x = end_pos.x - 20
                self.card_move_sound.play()
                self.card_move_sound.set_volume(
                    self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                self.move_card_animation(added_card_img, added_card_rect,
                                        (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                self.draw_computer_cards()[self.game.current_player_index]
                pygame.display.flip()
            self.game.plus2_card_clicked(self.game.players[0])
        elif self.game.current_card.type == 'reverse' and self.game.deck.len_card() >= 1:
            # 클릭했을 때 오른쪽 카드 이미지들 누락 방지를 위한 코드
            self.redraw_card(i, self.screen, card_rect, card_rect_list)

            if self.game.direction == 1:
                reverse_icon = pygame.image.load(
                    resource_path("./assets/counterclockwise.png"))
                reverse_icon = pygame.transform.scale(reverse_icon, (150, 150))
            elif self.game.direction == -1:
                reverse_icon = pygame.image.load(
                    resource_path("./assets/clockwise.png"))
                reverse_icon = pygame.transform.scale(reverse_icon, (150, 150))

            display_reverse_animation(self.screen, reverse_icon)

            self.game.reverse_card_clicked()

            # 다시 오른쪽카드들 그려지므로 삭제
            del card_rect_list[i+1: len(self.game.players[0].cards)]

        elif self.game.current_card.type == 'skip' and self.game.deck.len_card() >= 1:
            self.redraw_card(i, self.screen, card_rect, card_rect_list)
            skip_name = self.game.current_player_index + 1 if self.game.direction == 1 else len(self.game.players) - 1

            self.game.skip_card_clicked()
            display_skip_animation(self.screen, self.game.player_names[skip_name])

            del card_rect_list[i+1: len(self.game.players[0].cards)]
        elif self.game.current_card.type in range(1, 10) and self.game.deck.len_card() >= 1:
            # 그냥 number카드 일 때
            self.game.next_turn()
        else:
            self.game.deck.cards = self.game_deck_used_all()
            self.func_card_clicked(i, card_rect, chosen_card, card_rect_list)

    def handle_card_hover(self, card_rect_list):
        mouse_pos = pygame.mouse.get_pos()
        
        card_reacted = False
        # 키보드 인덱스 
        if self.setting.keys_idx == 2:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_RETURN:
                        if self.valid_play(self.game.players[0].cards[self.key_idx], self.game.current_card):
                            
                            print("game turn : " + str(self.game.turn_count))
                            chosen_card = self.game.players[0].cards[self.key_idx]
                            self.openned_cards.append(chosen_card)

                            # 클릭한 카드 pop
                            self.game.players[0].cards.pop(self.key_idx)

                            # 사운드 함수 호출
                            self.card_sound()

                            # 카드 이동 애니메이션
                            chosen_card_rect = card_rect_list[self.key_idx]
                            start_pos = card_rect_list[self.key_idx]
                            chosen_card_img = pygame.image.load(
                                chosen_card.front).convert_alpha()
                            self.move_card_animation(chosen_card_img, chosen_card_rect,(start_pos.x, start_pos.y), (self.screen_width*0.4, self.screen_height*0.25))

                            # 현재 카드 업데이트
                            self.game.current_card = self.openned_cards[-1]

                            self.func_card_clicked(
                                self.key_idx, card_rect_list[self.key_idx], chosen_card, card_rect_list)
                        else:
                            print("no")
                    elif event.key == pygame.K_LEFT:
                        self.key_idx -= 1
                        if self.key_idx < 0:
                            self.key_idx = 0
                    elif event.key == pygame.K_RIGHT:
                        self.key_idx += 1
                        if self.key_idx >= len(card_rect_list):
                            self.key_idx = len(card_rect_list) - 1
                    elif event.key == pygame.K_SPACE:
                        if self.game.current_player_index == 0:
                            print("game turn : " + str(self.game.turn_count))
                            self.process_deck_clicked(
                                self.deck_rect, card_rect_list[-1]) 
                        else:
                            Message(self.screen,
                                    "It's not your turn!", RED).draw()

            for i, card_rect in enumerate(card_rect_list):
                if i >= len(self.game.players[0].cards):
                    continue  # 유효하지 않은 인덱스를 건너뛰기
                card_front_img = pygame.image.load(self.game.players[0].cards[i].front).convert_alpha()

                if self.key_idx == i:
                    card_rect.top = self.screen_height * 0.75
                    if self.game.current_card is not None:
                        if self.valid_play(self.game.players[0].cards[i], self.game.current_card):
                            self.screen.blit(card_front_img, card_rect)
                        else:
                            darkened_image = self.apply_shadow(card_front_img)
                            self.screen.blit(darkened_image, card_rect)

                else:
                    card_rect.top = self.screen_height * 0.80
                    self.screen.blit(card_front_img, card_rect)
                    
        else:
            for i, card_rect in enumerate(card_rect_list):
                if i >= len(self.game.players[0].cards):
                    continue  # 유효하지 않은 인덱스를 건너뛰기
                card_front_img = pygame.image.load(
                    self.game.players[0].cards[i].front).convert_alpha()

                if not card_reacted and card_rect.collidepoint(mouse_pos):
                    card_rect.top = self.screen_height * 0.75
                    darkened_image = self.apply_shadow(card_front_img)
                    self.screen.blit(darkened_image, card_rect)
                    card_reacted = True
                    if self.game.current_card is not None:
                        if self.valid_play(self.game.players[0].cards[i], self.game.current_card):
                            self.screen.blit(card_front_img, card_rect)
                        # 카드 클릭 로직
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    print("game turn : " + str(self.game.turn_count))
                                    chosen_card = self.game.players[0].cards[i]
                                    self.openned_cards.append(chosen_card)

                                    # 클릭한 카드 pop
                                    self.game.players[0].cards.pop(i)

                                    # 사운드 함수 호출
                                    self.card_sound()

                                    # 카드 이동 애니메이션
                                    chosen_card_rect = card_rect_list[i]
                                    start_pos = card_rect_list[i]
                                    chosen_card_img = pygame.image.load(
                                        chosen_card.front).convert_alpha()
                                    self.move_card_animation(chosen_card_img, chosen_card_rect,(start_pos.x, start_pos.y), (self.screen_width*0.4, self.screen_height*0.25))

                                    # 현재 카드 업데이트
                                    self.game.current_card = self.openned_cards[-1]

                                    self.func_card_clicked(
                                        i, card_rect, chosen_card, card_rect_list)
                            

                else:
                    card_rect.top = self.screen_height * 0.80
                    self.screen.blit(card_front_img, card_rect)

    def display_player_cards(self):
        card_rect_list = []

        for i, card in enumerate(self.game.players[0].cards):
            card_front_img = pygame.image.load(card.front).convert_alpha()
            card_rect = card_front_img.get_rect()
            if i == 0:
                card_rect.left = self.screen_width * 0.05
                card_rect.top = self.screen_height * 0.80
            else:
                card_rect.left = card_rect_list[i -
                                                1].left + (self.screen_width * 0.05)
                card_rect.top = self.screen_height * 0.80

            card_rect_list.append(card_rect)

        self.handle_card_hover(card_rect_list)
        return card_rect_list

    def current_card_color(self):
        card_color = self.game.current_card.color
        current_card_rect = pygame.Rect(
            self.screen_width*0.75 - 60, 20, 40, 40)
        if self.game.color_weak_mode == True:
            idx = 0
        else:
            idx = 1
        if card_color == 'red':
            pygame.draw.rect(self.screen, RED if idx ==
                             1 else W_RED, current_card_rect)
        elif card_color == 'blue':
            pygame.draw.rect(self.screen, BLUE if idx ==
                             1 else W_BLUE, current_card_rect)
        elif card_color == 'green':
            pygame.draw.rect(self.screen, GREEN if idx ==
                             1 else W_GREEN, current_card_rect)
        elif card_color == 'yellow':
            pygame.draw.rect(self.screen, YELLOW if idx ==
                             1 else W_YELLOW, current_card_rect)

    def who_is_current_player(self):
        player = font.render(
            self.game.players[self.game.current_player_index].name, True, WHITE)
        player_rect = player.get_rect()
        player_rect.centerx = round(self.screen_width * 0.75 * 0.5)
        player_rect.y = 20
        self.screen.blit(player, player_rect)

    def unobutton(self):
        unobutton_img = pygame.image.load(resource_path(
            './assets/unobutton.png')).convert_alpha()
        unobutton_rect = unobutton_img.get_rect()
        unobutton_rect.centerx = round(self.screen_width*0.75*0.5)
        unobutton_rect.y = self.screen_height * 0.45
        self.screen.blit(unobutton_img, unobutton_rect)
        return unobutton_rect

    def move_card_animation(self, card_img, card_rect, start_pos, end_pos, duration=500):
        # global openned_cards
        start_time = pygame.time.get_ticks()
        elapsed_time = 0
        distance = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

        while elapsed_time < duration:
            elapsed_time = pygame.time.get_ticks() - start_time
            progress = min(elapsed_time / duration, 10)
            new_pos = start_pos[0] + distance[0] * \
                progress, start_pos[1] + distance[1] * progress
            card_rect.x, card_rect.y = new_pos
            self.screen.blit(card_img, (card_rect.left, card_rect.top))
            pygame.display.flip()
            draw_game_screen(self)
            self.uno_button.draw()
            self.draw_deck()
            if self.openned_cards[-1] == self.game.current_card:
                draw_card_front(
                    self.screen, self.openned_cards[-1], self.screen_height * 0.25, card_loc)
            else:
                draw_card_front(
                    self.screen, self.openned_cards[-2], self.screen_height * 0.25, card_loc)
            self.current_card_color()
            if self.game.current_player_index != 0:
                self.who_is_current_player()
            self.draw_computer_cards()
            self.display_player_cards()

    def process_deck_clicked(self, deck_rect, end_pos):
        popped_card = self.game.deck.pop_card()
        end_pos.x = end_pos.x + (self.screen_width * 0.05)
        card_img = pygame.image.load(popped_card.front).convert_alpha()
        card_rect = card_img.get_rect()

        self.card_move_sound.play()
        self.card_move_sound.set_volume(
            self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
        self.move_card_animation(
            card_img, card_rect, (deck_rect.x, deck_rect.y), (end_pos.x, end_pos.y))
        self.game.players[0].cards.append(popped_card)
        print(
            f"\n{self.game.players[self.game.current_player_index].name}이 deck에서 카드를 한 장 받습니다.")
        # 다음 턴으로 넘김
        self.game.next_turn()

    def computer_function_animation(self):
        card_rect_list = []
        player_list = self.display_player_cards()[-1]
        computers_list = self.draw_computer_cards()
        card_rect_list.append(player_list)
        card_rect_list.append(computers_list)
        if self.game.direction == 1:
                    next_idx = self.game.current_player_index
                    if next_idx == len(self.game.player_names) - 1:
                        next_idx = 0
                        end_pos = card_rect_list[next_idx]
                    else:
                        end_pos = card_rect_list[1][next_idx][0]
        else:
            next_idx = self.game.current_player_index - 2
            if next_idx == 0:
                next_idx = 0 
                end_pos = card_rect_list[1][next_idx][0]
            elif next_idx == -1:
                next_idx = 0 
                end_pos = card_rect_list[next_idx]
            else:
                end_pos = card_rect_list[1][next_idx][0]

        return end_pos

    # 컴퓨터가 black card 낼 때    
    def computer_black_card(self, chosen_card):
        choiced_color = self.game.players[self.game.current_player_index].black_card_clicked()
        self.game.current_card.color = choiced_color
        if chosen_card.type == 'wildcard' and self.game.deck.len_card() >= 1:
            self.game.wildcard_card_clicked(choiced_color)
        elif chosen_card.type == '+4' and self.game.deck.len_card() >= 4:
            end_pos = self.computer_function_animation()
                    
            for i in range(4):
                added_card = self.game.deck.cards[-(i+1)]
                added_card_img = pygame.image.load(
                    added_card.front).convert_alpha()
                added_card_rect = added_card_img.get_rect()
                start_pos = self.draw_deck()
                end_pos.x = end_pos.x - (self.screen_width * 0.03)
                self.card_move_sound.play()
                self.card_move_sound.set_volume(
                    self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                self.move_card_animation(added_card_img, added_card_rect,
                                        (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                self.screen.blit(added_card_img, (end_pos.x, end_pos.y))
            self.game.plus4_card_clicked(choiced_color)
        elif chosen_card.type == 'bomb' and self.game.deck.len_card() >= (3 * (len(self.game.players)-1)):
            bomb_icon = pygame.image.load(
                resource_path("./assets/bomb.png"))
            bomb_icon = pygame.transform.scale(bomb_icon, (250, 250))
            display_bomb_animation(self.screen, bomb_icon)
            # player한테 bomb
            end_pos = self.display_player_cards()[-1]
            for i in range(3):
                added_card = self.game.deck.cards[-(i+1)]
                added_card_img = pygame.image.load(
                    added_card.front).convert_alpha()
                added_card_rect = added_card_img.get_rect()
                start_pos = self.draw_deck()
                end_pos.x = end_pos.x + (self.screen_width * 0.05)
                self.card_move_sound.play()
                self.card_move_sound.set_volume(
                    self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                self.move_card_animation(added_card_img, added_card_rect,(start_pos.x, start_pos.y), (end_pos.x, end_pos.y))

            for i in range(len(self.game.players) - 1):
                if i != (self.game.current_player_index-1):
                    end_pos = self.draw_computer_cards()[i][-1]
                    for j in range(3):
                        added_card = self.game.deck.cards[-(j+1)]
                        added_card_img = pygame.image.load(
                            added_card.back).convert_alpha()
                        added_card_rect = added_card_img.get_rect()
                        start_pos = self.draw_deck()
                        end_pos.x = end_pos.x - 20
                        self.card_move_sound.play()
                        self.card_move_sound.set_volume(
                            self.setting.volume * self.setting.effect_volume * 0.01)
                        self.move_card_animation(added_card_img, added_card_rect,
                                                (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                        pygame.display.flip()
                
            self.game.bombcard_card_clicked(choiced_color)

        elif chosen_card.type == 'all' and self.game.deck.len_card() >= 1:
            # 다음 turn player와 card 바꿈
            current_name = self.game.players[self.game.current_player_index].name
            target_name = self.game.players[(self.game.current_player_index + 1) % len(self.game.players)].name
            all_change_icon = pygame.image.load(
                resource_path("./assets/all_change.png"))
            all_change_icon = pygame.transform.scale(
                all_change_icon, (200, 200))
            display_all_change_animation(
                self.screen, all_change_icon, current_name, target_name)

            self.game.change_all_clicked(((self.game.current_player_index + 1) % len(self.game.players)), choiced_color)

    # 컴퓨터가 기능 카드 낼 때
    def computer_function_card(self):
        if self.game.current_card.type == 'all':
            self.computer_black_card(self.game.current_card)
        elif self.game.current_card.type == 'wildcard':
            self.computer_black_card(self.game.current_card)
        elif self.game.current_card.type == '+4':
            self.computer_black_card(self.game.current_card)
        elif self.game.current_card.type == 'bomb':
            self.computer_black_card(self.game.current_card)

        elif self.game.current_card.type == '+2' and self.game.deck.len_card() >= 2:
            end_pos = self.computer_function_animation()

            for i in range(2):
                added_card = self.game.deck.cards[-(i+1)]
                added_card_img = pygame.image.load(
                    added_card.front).convert_alpha()
                added_card_rect = added_card_img.get_rect()
                start_pos = self.draw_deck()
                end_pos.x = end_pos.x - (self.screen_width * 0.03)
                self.card_move_sound.play()
                self.card_move_sound.set_volume(
                    self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                self.move_card_animation(added_card_img, added_card_rect,
                                        (start_pos.x, start_pos.y), (end_pos.x, end_pos.y))
                self.screen.blit(added_card_img, (end_pos.x, end_pos.y))
            self.game.plus2_card_clicked(
                self.game.players[self.game.current_player_index])
        elif self.game.current_card.type == 'reverse' and self.game.deck.len_card() >= 1:
            if self.game.direction == 1:
                reverse_icon = pygame.image.load(
                    resource_path("./assets/counterclockwise.png"))
                reverse_icon = pygame.transform.scale(reverse_icon, (200, 200))
            else:
                reverse_icon = pygame.image.load(
                    resource_path("./assets/clockwise.png"))
                reverse_icon = pygame.transform.scale(reverse_icon, (200, 200))
            display_reverse_animation(self.screen, reverse_icon)
            self.game.reverse_card_clicked()
        elif self.game.current_card.type == 'skip' and self.game.deck.len_card() >= 1:
            # 게임 function card 버그 고쳐지면 수정 --> 지금은 애니메이션만 일시적으로 해놓음
            display_skip_animation(self.screen, self.game.players[(
                self.game.current_player_index + 1) % len(self.game.players)].name)
            self.game.skip_card_clicked()
        elif self.game.current_card.type in range(1, 10) and self.game.deck.len_card() >= 1:
            self.game.next_turn()
        else:
            self.game.deck.cards = self.game_deck_used_all()
            self.computer_function_card()


    def game_deck_used_all(self, event=None):
        cards_list = []
        while len(self.openned_cards) > 1:
                        card = self.openned_cards.pop(0)
                        self.game.deck.cards.append(card)
                        cards_list = self.game.deck.cards.copy()
                        shuffle(cards_list)
        print("openned cards moved to deck.")
        self.deck_rect = self.draw_deck()
        return cards_list
        # winner_box = pygame.Rect(self.screen_width * 0.05, self.screen_height * 0.2,
        #                                     self.screen_width * 0.9, self.screen_height * 0.6)
        # pygame.draw.rect(self.screen, DARK_GRAY, winner_box)
        # Message(self.screen, "FINISH A TIE", WHITE).winner_draw()
        # # Message(self.screen, "Press Enter to go to menu", WHITE).press_esc_draw()
        # self.timerFlag = False
        # for event in pygame.event.get():
        #     while True:
        #         if event.type == pygame.KEYDOWN:
        #             if event.key == pygame.K_RETURN:
        #                 return "menu"

    def running(self):

        
        

        # 카드 초기 세팅
        if isinstance(self.game, StoryGameB):
            while test_deal_cards(self.game) == False:
                self.game.deal_cards()
        else:
            self.game.deal_cards()

        pygame.mixer.music.load(resource_path('./assets/background.mp3'))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(
            self.setting.volume * 0.01 * self.setting.back_volume * 0.01)

        # players[0] 카드 출력
        print(f"\n{self.game.players[0].name}'s cards:")
        for i in range(len(self.game.players[0].cards)):
            print(self.game.players[0].cards[i])

        # global openned_cards
        flip_card2 = True
        running = True
        paused = False

        draw_game_screen(self)
        self.deck_rect = self.draw_deck()
        self.draw_computer_cards()

        self.uno_button.draw()
        card_rect_list = self.display_player_cards()

        # 피클 세팅

        if os.path.exists(resource_path('game_state.pkl')):
            with open(resource_path('game_state.pkl'), 'rb') as f:
                game_state = pickle.load(f)
                print("load pickle")
            self.game = game_state
            self.game.color_weak_mode = self.setting.color_weak
        

        if os.path.exists(resource_path('achievements.pkl')):
            with open(resource_path('achievements.pkl'), 'rb') as f:
                achievements = pickle.load(f)
                print("load achievements pickle")
            self.achievements = achievements
        else:
            self.achievements = None
            print("No achievements")

        print("current card : "+str(self.game.current_card))

        self.flip_deck_card(flip_card2)

        while running:
            dt = self.clock.tick(60)/1000.0
            

            for event in pygame.event.get():
            # event = pygame.event.get()
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
                    del self
                    return "exit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("esc")
                        self.game.color_weak_mode = self.setting.color_weak
                        paused = True
                        with open(resource_path("game_state.pkl"), "wb") as f:
                            pickle.dump(self.game, f)
                        return "pause"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.deck_rect.collidepoint(event.pos):
                        if self.game.current_player_index == 0:
                            print("game turn : " + str(self.game.turn_count))
                            self.process_deck_clicked(
                                self.deck_rect, card_rect_list[-1])
                        else:
                            Message(self.screen,
                                    "It's not your turn!", RED).draw()
                    if self.uno_button.rect.collidepoint(event.pos):
                        print("UNO button clicked - Player")
                        if len(self.game.players[0].cards) == 1:
                            self.uno_button_pressed = True
                            Message(self.screen, "UNO BUTTON CLICKED - YOU", BLUE).draw()
                            self.game.uno_button_clicked(0)
                        else:
                            Message(self.screen, "WRONG UNO", BLUE).draw()

                self.uiManager.process_events(event)

            if paused is True:
                return "pause"

            else:
                draw_game_screen(self)
                self.uno_button.draw()
                self.deck_rect = self.draw_deck()
                self.current_card_color()
                self.flip_deck_card(None)
                self.draw_computer_cards()
                card_rect_list = self.display_player_cards()

                player_with_one_card = [
                    player for player in self.game.players if len(player.cards) == 1]
                player_with_no_card = [
                    player for player in self.game.players if len(player.cards) == 0]

                if player_with_one_card:

                    if randint(0, 1) and not self.uno_button_pressed:
                        pygame.display.flip()
                        pygame.time.delay(int(random()*300))
                        who_pressed_uno = choice(self.game.players[1:])
                        uno_index = self.game.players.index(who_pressed_uno)
                        self.game.uno_button_clicked(uno_index)
                        self.uno_button_pressed = True
                        Message(self.screen, f"UNO BUTTON CLICKED - {who_pressed_uno.name}", RED).draw()
                        print(f"UNO button clicked - {who_pressed_uno.name}")

                if not player_with_one_card and self.uno_button_pressed:
                    self.uno_button_pressed = False

                if player_with_no_card:
                    achievement_message = []
                    if player_with_no_card[0].name == self.game.player_names[0]:
                        if isinstance(self.game, StoryGameA):
                            self.achievements[1].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[1].name} COMPLETED", WHITE))
                        elif isinstance(self.game, StoryGameB):
                            self.achievements[2].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[2].name} COMPLETED", WHITE))
                        elif isinstance(self.game, StoryGameC):
                            self.achievements[3].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[3].name} COMPLETED", WHITE))
                        elif isinstance(self.game, StoryGameD):
                            self.achievements[4].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[4].name} COMPLETED", WHITE))
                        else:
                            self.achievements[0].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[0].name} COMPLETED", WHITE))

                        if self.game.turn_count <= 10:
                            self.achievements[5].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[5].name} COMPLETED", WHITE))
                        elif self.game.turn_count <= 15:
                            self.achievements[6].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[6].name} COMPLETED", WHITE))
                        elif self.game.turn_count <= 20:
                            self.achievements[7].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[7].name} COMPLETED", WHITE))

                        if self.game.skill_card_used  == False:
                            self.achievements[8].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[8].name} COMPLETED", WHITE))
                        if self.game.uno_by_others == True:
                            self.achievements[9].complete()
                            achievement_message.append(Message(self.screen, f"{achievements[9].name} COMPLETED", WHITE))

                        with open(resource_path('achievements.pkl'), 'wb') as f:
                            pickle.dump(self.achievements, f, pickle.HIGHEST_PROTOCOL)
                            print("achievements save!!")
                            # pkl 바로 적용 안돼서 직접 객체를 가져와서 업데이트 함 
                            self.achievement_page.achievements = self.achievements
                            
                    winner_box = pygame.Rect(self.screen_width * 0.05, self.screen_height * 0.2,
                                            self.screen_width * 0.9, self.screen_height * 0.6)
                    pygame.draw.rect(self.screen, DARK_GRAY, winner_box)
                    Message(
                        self.screen, f"{player_with_no_card[0].name} WIN", WHITE).winner_draw()
                    if len(achievement_message) > 0:
                        for i, message in enumerate(achievement_message):
                            message.draw_achievement(i)
                    self.timerFlag = False
                    pygame.time.delay(3000)
                    # 우승자 표시하고 paused page로
                    return "pause"

                # 우노 게임카드 다 썼을 때
                # TODO : 카드 다 썼을 때, openned card에서 deck으로 카드 옮기기 -> 수정 완료
                while self.game.deck.len_card() == 0:                  
                    self.game.deck.cards = self.game_deck_used_all(event)
                    deck_rect = self.draw_deck()

                while self.game.current_player_index != 0 and self.game.deck.len_card() >= 1:
                    if self.game.players[self.game.current_player_index].can_play(self.game.current_card):
                        print(
                            f"\n현재 {self.game.players[self.game.current_player_index].name}의 턴입니다.")
                        # 현재 플레이어 화면 출력
                        pygame.display.flip()
                        self.who_is_current_player()
                        draw_card_front(
                            self.screen, self.openned_cards[-1], self.screen_height * 0.25, card_loc)

                        if len(self.game.players[self.game.current_player_index].cards) == 0:
                            print("Computer Win!!")

                        computer_card_rect_list = self.draw_computer_cards()

                        popped_card = self.game.players[self.game.current_player_index].play_card(self.game)

                        # TODO popped_card가 list일 때 처리
                        if type(popped_card) == list:
                            for card in popped_card:
                                # card_back_img = pygame.image.load(card.back).convert_alpha()
                                card_rect = computer_card_rect_list[(self.game.current_player_index - 1)][0]
                                self.openned_cards.append(card)

                                start_pos = card_rect
                                self.card_move_sound.play()
                                self.card_move_sound.set_volume(
                                    self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                                card_back_img = pygame.image.load(card.back).convert_alpha()
                                self.move_card_animation(card_back_img, card_rect,
                                                         (start_pos.x, start_pos.y),
                                                         (self.screen_width * 0.4, self.screen_height * 0.25))
                                # current card 업데이트
                                self.game.current_card = self.openned_cards[-1]

                                # function card 일 때
                                self.computer_function_card()

                        else:
                            popped_card_rect = computer_card_rect_list[(self.game.current_player_index - 1)][0]
                            self.openned_cards.append(popped_card)

                            start_pos = popped_card_rect
                            self.card_move_sound.play()
                            self.card_move_sound.set_volume(
                                self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                            popped_card_back_img = pygame.image.load(popped_card.back).convert_alpha()
                            self.move_card_animation(popped_card_back_img, popped_card_rect,
                                                     (start_pos.x, start_pos.y), (self.screen_width*0.4, self.screen_height*0.25))
                            # current card 업데이트
                            self.game.current_card = self.openned_cards[-1]

                            # function card 일 때
                            self.computer_function_card()

                    elif self.game.deck.len_card() >= 1:
                        print(
                            f"\n현재 {self.game.players[self.game.current_player_index].name}의 턴입니다.")

                        # 현재 플레이어 화면 출력
                        pygame.display.flip()
                        self.who_is_current_player()
                        draw_card_front(
                            self.screen, self.openned_cards[-1], self.screen_height * 0.25, card_loc)
                            
                        computer_card_rect_list = self.draw_computer_cards()

                        print(
                            f"\n{self.game.players[self.game.current_player_index].name}이 deck에서 카드를 한 장 받습니다.")
                        self.game.players[self.game.current_player_index].draw_card(
                            self.game.deck)
                        new_computer_card = self.game.players[self.game.current_player_index].cards[-1]
                        new_computer_card_img = pygame.image.load(
                            new_computer_card.back).convert_alpha()
                        new_computer_card_rect = new_computer_card_img.get_rect()
                        end_pos = computer_card_rect_list[self.game.current_player_index - 1][-1]
                        end_pos.x = end_pos.x - 20
                        self.card_move_sound.play()
                        self.card_move_sound.set_volume(
                            self.setting.volume * 0.01 * self.setting.effect_volume * 0.01)
                        self.move_card_animation(new_computer_card_img, new_computer_card_rect,
                                                 (self.deck_rect.x, self.deck_rect.y),
                                                 (end_pos.x, end_pos.y))
                        self.game.next_turn()
                    else:
                        self.game.deck.cards = self.game_deck_used_all()
                        self.deck_rect = self.draw_deck()

                self.uiManager.update(dt)
                self.uiManager.draw_ui(self.screen)
                pygame.display.update()

        return "game"
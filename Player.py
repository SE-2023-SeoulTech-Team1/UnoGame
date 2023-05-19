import time
import pygame
from random import random, choice, randint

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def draw_card(self, deck):
        card = deck.pop_card()
        self.cards.append(card)
        
    def play_card(self, card_index):
        return self.cards.pop(card_index)

class Computer:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def draw_card(self, deck):
        # pygame.display.flip()
        pygame.time.delay(int(random()*1000))
        card = deck.pop_card()
        self.cards.append(card)

    def can_play(self, current_card):
        card_idx_can_play = []
        for idx, card in enumerate(self.cards):
            if card.color == current_card.color or card.type == current_card.type or card.color == "black":
                card_idx_can_play.append(idx)
        return card_idx_can_play

    def play_card(self, game):
        pygame.time.delay(int(random()*1000))
        card_idx_can_play = self.can_play(game.current_card)
        return self.cards.pop(choice(card_idx_can_play))
    
    def black_card_clicked(self):
        color_list = ['red', 'green', 'yellow', 'blue']
        return choice(color_list)

    # def click_uno_button(self, game):
    #     # TODO 지연시간 두기
    #     pygame.display.flip()
    #     pygame.time.delay(int(random()*3000))
    #     game.uno_button_clicked(1)


class AlienA(Computer):
    def __init__(self, name):
        super().__init__(name)

    def number_card_can_play(self, current_card):
        number_card_idx_can_play_color = []
        number_card_idx_can_play_type = []
        for idx, card in enumerate(self.cards):
            if card.color == current_card.color:
                number_card_idx_can_play_color.append(idx)
            elif card.type == current_card.type:
                number_card_idx_can_play_type.append(idx)
        return number_card_idx_can_play_color, number_card_idx_can_play_type

    def play_card(self, game):
        """
        컴퓨터 플레이어가 숫자카드를 2개 이상 낼 수 있음
        """
        number_card_idx_can_play_color, number_card_idx_can_play_type = self.number_card_can_play(game.current_card)
        if number_card_idx_can_play_color and number_card_idx_can_play_type:
            randint(0, 1)
        elif number_card_idx_can_play_color:
            for idx in number_card_idx_can_play_color:
                self.cards.pop(idx)
            return number_card_idx_can_play_color
        elif number_card_idx_can_play_type:
            for idx in number_card_idx_can_play_type:
                self.cards.pop(idx)
            return number_card_idx_can_play_type
        else:
            card_idx_can_play = self.can_play(game.current_card)
            return self.cards.pop(card_idx_can_play[0])


class AlienB(Computer):
    def __init__(self, name):
        super().__init__(name)

    def play_card(self, game):
        """
        컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
        """

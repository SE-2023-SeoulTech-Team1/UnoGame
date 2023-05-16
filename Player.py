import time
import pygame
from random import random, choice

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
        # pygame.time.delay(int(random()*3000))
        card = deck.pop_card()
        self.cards.append(card)

    def can_play(self, current_card):
        card_idx_can_play = []
        for idx, card in enumerate(self.cards):
            if card.color == current_card.color or card.type == current_card.type or card.color == "black":
                card_idx_can_play.append(idx)
        return card_idx_can_play

    def play_card(self, game):
        # pygame.time.delay(int(random()*3000))
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


class StoryComputerA(Computer):
    def __init__(self, name):
        super().__init__(name)

    def play_card(self, game):
        """
        컴퓨터 플레이어가 같은 색깔카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
        """
        card_idx_can_play = self.can_play(game.current_card)
        card_idx_same_color = []
        card_same_color = []
        for i in range(len(card_idx_can_play)):
            if self.cards[card_idx_can_play[i]].color == game.current_card.color:
                card_idx_same_color.append(card_idx_can_play[i])
        print("card_idx_same_color", card_idx_same_color)
        print("card_idx_can_play", card_idx_can_play)
        if len(card_idx_same_color) >= 2:
            for i in range(len(card_idx_same_color)):
                card_same_color.append(self.cards[card_idx_same_color[i]])
                self.cards.pop(card_idx_same_color[i])
            return card_same_color
        elif len(card_idx_can_play) >= 2:
            return self.cards.pop(choice(card_idx_can_play))
        else:
            return self.cards.pop(card_idx_can_play[0])

        # while self.can_play(game.current_card):
        #     card_idx_can_play = self.can_play(game.current_card)
        #     if len(card_idx_can_play) >= 2:
        #         return self.cards.pop(choice(card_idx_can_play))
        #     else:
        #         return self.cards.pop(card_idx_can_play[0])

class StoryComputerB(Computer):
    def __init__(self, name):
        super().__init__(name)

    def play_card(self, game):
        """
        컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
        """
        while self.can_play(game.current_card):
            card_idx_can_play = self.can_play(game.current_card)
            if len(card_idx_can_play) >= 2:
                return self.cards.pop(choice(card_idx_can_play))
            else:
                return self.cards.pop(card_idx_can_play[0])
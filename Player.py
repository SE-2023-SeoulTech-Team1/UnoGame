import time
import pygame
from random import random, choice
from Card import *


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


class StoryComputerB(Computer):
    def __init__(self, name):
        super().__init__(name)

    def can_play_combo(self, current_card):
        if current_card.color == "black":
            return False
        combination = [idx for idx, card in enumerate(self.cards) if (
            card.color == current_card.color and card.type == SPECIAL_CARD_TYPES)]
        print(combination)
        if combination:
            return combination
        else:
            return False

    def play_card(self, game):
        # pygame.time.delay(int(random()*3000))
        combination = self.can_play_combo(game.current_card)
        if combination:
            print("combo")
            for idx in combination:
                self.cards.pop(idx)
            return combination
        else:
            card_idx_can_play = self.can_play(game.current_card)
            return self.cards.pop(choice(card_idx_can_play))

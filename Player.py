import time
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
        time.sleep(random() * 3)
        card = deck.pop_card()
        self.cards.append(card)

    def can_play(self, current_card):
        card_idx_can_play = []
        for idx, card in enumerate(self.cards):
            if card.color == current_card.color or card.type == current_card.type or card.color == "black":
                card_idx_can_play.append(idx)
        return card_idx_can_play

    def play_card(self, game):
        time.sleep(random() * 3)
        card_idx_can_play = self.can_play(game.current_card)
        return self.cards.pop(choice(card_idx_can_play))
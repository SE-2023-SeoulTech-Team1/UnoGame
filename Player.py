from Card import *
from random import shuffle

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.auto = False
        
    def draw_card(self, deck):
        card = deck.pop_card()
        self.cards.append(card)
        
    def play_card(self, card_index):
        return self.cards.pop(card_index)

from random import shuffle, choices

COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES
BLACK_CARD_TYPES = ['wildcard', '+4', 'bomb', 'all']
ALL_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES

class Card:
    def __init__(self, color, type, color_weak_mode=False):
        if color not in ALL_COLORS:
            print("Invalid Card Color.")
            exit(-1)
        if type not in ALL_TYPES:
            print("Invalid Card Type")
            exit(-1)

        self.color = color
        self.type = type
        if color_weak_mode:
            self.front = f"./assets/colorWeakCards/{self.color}{self.type}.png"
            self.back = "./assets/colorWeakCards/unoCardBack.png"
        else:
            self.front = f"./assets/cards/{self.color}{self.type}.png"
            self.back = "./assets/cards/unoCardBack.png"

    def __str__(self):
        return f'Uno Card Object: {self.color} {self.type}'


class Deck:
    def __init__(self, cards):
        if len(cards) < 1:
            print("At least one more cards should be in deck.")
            exit(-1)
        self.cards = cards
        
    def len_card(self):
        return len(self.cards)

    def pop_card(self):
        return self.cards.pop()

    def shuffle(self):
        shuffle(self.cards)

    def choice_card(self):
        weights = [1 / 68] * 36 + [2 / 68] * 32
        idx = choices(range(len(self.cards)), weights=weights)
        return self.cards.pop(idx)

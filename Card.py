COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES
BLACK_CARD_TYPES = ['wildcard', '+4']
ALL_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES


class Card:
    def __init__(self, color, type):
        if color not in ALL_COLORS:
            print("Invalid Card Color.")
            exit(-1)
        if type not in ALL_TYPES:
            print("Invalid Card Type")
            exit(-1)

        self.color = color
        self.type = type

    def __str__(self):
        return f'Uno Card Object: {self.color} {self.type}'


class Deck:
    def __init__(self, cards):
        if len(cards) < 1:
            print("At least one more cards should be in deck.")
            exit(-1)
        self.cards = cards

    def pop_card(self):
        return self.cards.pop()

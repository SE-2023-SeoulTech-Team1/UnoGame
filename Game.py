from Card import *
from Player import *

class Game:
    def __init__(self, players):

        if not players:
            print("Number of Players should be at least one.")
            exit(-1)

        cards = [Card(color, type) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type) for type in BLACK_CARD_TYPES]
        shuffle(cards)

        self.deck = Deck(cards)
        self.players = players
        self.current_player_index = 0
        self.current_card = None

    def start(self):
        # 카드 7장 나누기
        for i in range(7):
            for player in self.players:
                player.draw_card(self.deck)
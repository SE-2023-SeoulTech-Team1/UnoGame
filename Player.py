class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        
    def draw_card(self, deck):
        card = deck.draw_card()
        self.cards.append(card)
        
    def play_card(self, card_index):
        return self.cards.pop(card_index)

        
class Game:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.current_player_index = 0
        self.current_card = None
        
    def start(self):
        # 카드 7장 나누기
        for i in range(7):
            for player in self.players:
                player.draw_card(self.deck)

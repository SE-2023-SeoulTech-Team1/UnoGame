from random import random
from Card import *
from Game import Game
from Player import *


class StoryGameA(Game):
    """
    컴퓨터 플레이어가 색깔카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien"], color_weak_mode)

    def deal_cards(self):
        # TODO 테스트 코드 작성
        for i in range(7):
            for player in self.players:
                if isinstance(player, Computer):
                    player.cards.append(self.deck.choice_card())
                else:
                    player.cards.append(self.deck.pop_card())

class StoryGameB(Game):
    """
    첫 분배시 컴퓨터 플레이어가 기술 카드를 50% 더 높은 확률로 받게 됨.
    컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien"], color_weak_mode)

    def test_probability(self):
        computer = self.players[1]
        cards = [Card(color, type, color_weak_mode=False)
                 for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, color_weak_mode=False)
                  for type in BLACK_CARD_TYPES]
        for i in range(100):
            deck = Deck(cards)
            self.deal_cards()
        print("Number of skill cards from Computer: ",
              len([card for card in self.players[1].cards if card.type in SPECIAL_CARD_TYPES]))
        print("Number of skill cards from Player: ",
              len([card for card in self.players[0].cards if card.type in SPECIAL_CARD_TYPES]))


    def deal_cards(self):
        # TODO 테스트 코드 작성
        for i in range(7):
            for player in self.players:
                if isinstance(player, Computer):
                    if random() < 0.5:
                        player.cards.append(self.deck.pop_skill_card())
                    else:
                        player.cards.append(self.deck.pop_number_card())
                else:
                    player.cards.append(self.deck.pop_card())

class StoryGameC(Game):
    """
    3명의 컬퓨터 플레이어와 대전
    첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien1", "Alien2", "Alien3"], color_weak_mode)

    def deal_cards(self):
        for i in range(12):
            for player in self.players:
                    player.cards.append(self.deck.pop_card())


class StoryGameD(Game):
    """
    2명의 컴퓨터 플레이어와 대전
    매 5턴마다 낼 수 있는 카드의 색상이 무작위로 변경됨
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien1", "Alien2"], color_weak_mode)

    # TODO 매 5턴마다 낼 수 있는 카드 색상 무작위 변경
    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            self.current_card.color = random.choice(["red", "blue", "green", "yellow", "black"])
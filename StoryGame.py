from random import choice
from Card import *
from Game import Game
from Player import *


class StoryGameA(Game):
    """
    컴퓨터 플레이어가 숫자 카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien"], color_weak_mode)
        self.player_names = ["Player", "Alien"]
        self.players = [Player(self.player_names[0])] + [StoryComputerA(name) for name in self.player_names[1:]]

    def deal_cards(self):
        cards = [Card(color, type, self.color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, self.color_weak_mode) for type in BLACK_CARD_TYPES]
        # TODO 테스트 코드 작성
        for i in range(7):
            for player in self.players:
                player.cards.append(self.deck.pop_card())


class StoryGameB(Game):
    """
    첫 분배시 컴퓨터 플레이어가 기술 카드를 50% 더 높은 확률로 받게 됨.
    컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
    """
    def __init__(self, color_weak_mode=False):
        self.player_names = ["Player", "Alien"]
        super().__init__(["Player", "Alien"], color_weak_mode)
        self.players = [Player(self.player_names[0])] + [StoryComputerB(name) for name in self.player_names[1:]]

    def deal_cards(self):
        # cards = [Card(color, type, self.color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        # cards += [Card("black", type, self.color_weak_mode) for type in BLACK_CARD_TYPES]
        # TODO 테스트 코드 작성
        for i in range(7):
            for player in self.players:
                if isinstance(player, Computer):
                    player.cards.append(self.deck.choice_card())
                else:
                    player.cards.append(self.deck.pop_card())


class StoryGameC(Game):
    """
    3명의 컬퓨터 플레이어와 대전
    첫 카드를 제외하고 모든 카드를 같은 수만큼 플레이어들에게 분배
    """
    def __init__(self, color_weak_mode=False):
        super().__init__(["Player", "Alien1", "Alien2", "Alien3"], color_weak_mode)
        self.player_names = ["Player", "Alien1", "Alien2", "Alien3"]

    def deal_cards(self):
        cards = [Card(color, type, self.color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, self.color_weak_mode) for type in BLACK_CARD_TYPES]
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
        self.player_names = ["Player", "Alien1", "Alien2"]

    # TODO 매 5턴마다 낼 수 있는 카드 색상 무작위 변경
    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        self.turn_count += 1
        if self.turn_count % 5 == 0:
            self.current_card.color = choice(["red", "blue", "green", "yellow"])

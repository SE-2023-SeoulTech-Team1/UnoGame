from Card import *
from Game import Game
from Player import *


class StoryGameA(Game):
    """
    첫 분배시 컴퓨터 플레이어가 기술 카드를 50% 더 높은 확률로 받게 됨.
    컴퓨터 플레이어가 거꾸로 진행과 건너 뛰기 등의 기술카드를 적절히 조합하여 2~3장 이상의 카드를 한 번에 낼 수 있는 콤보를 사용.
    """
    def __init__(self, player_names, color_weak_mode=False):
        super().__init__(player_names, color_weak_mode)

    def deal_cards(self):
        cards = [Card(color, type, self.color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, self.color_weak_mode) for type in BLACK_CARD_TYPES]
        # TODO 테스트 코드 작성
        for i in range(7):
            for player in self.players:
                if isinstance(player, Computer):
                    player.cards.append(self.deck.choice_card())
                else:
                    player.cards.append(self.deck.pop_card())

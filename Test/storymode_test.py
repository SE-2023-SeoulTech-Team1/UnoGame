import pytest
from Card import *
from StoryGame import *

def test_probability():
    skill_card_cnt_computer = 0
    skill_card_cnt_player = 0
    cards = [Card(color, type, color_weak_mode=False)
             for type in COLOR_CARD_TYPES for color in COLORS]
    cards += [Card("black", type, color_weak_mode=False)
              for type in BLACK_CARD_TYPES]
    for i in range(150):
        storygameB = StoryGameB()
        # storygameB.deck = Deck(cards)
        storygameB.deal_cards()
        skill_card_cnt_computer += len([card for card in storygameB.players[1].cards if card.type in SPECIAL_CARD_TYPES])
        skill_card_cnt_player += len([card for card in storygameB.players[0].cards if card.type in SPECIAL_CARD_TYPES])
    assert skill_card_cnt_computer > (skill_card_cnt_player + skill_card_cnt_computer) * 0.6

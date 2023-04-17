import unittest
import GamePage
from Game import *


class card_test(unittest.TestCase):

    def test_deck_len(self):
        game = Game(Player("Player"))
        game.reset_deck(self)
        self.assertEqual(game.deck.len_card(), 50)

    def test_players_init_setting(self):
        game = Game([Player("Player"), Computer("Computer")])
        game.deal_cards()
        self.assertEqual(len(game.players[0].cards), 7)

if __name__ == '__main__':
    unittest.main()
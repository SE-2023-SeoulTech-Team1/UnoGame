import unittest
from GamePage import *
from Setting import *
from Game import *
import pickle
import time
import random
from unittest.mock import MagicMock, patch




class card_test(unittest.TestCase):

    def test_deck_len(self):
        game = Game(Player("Player"))
        game.reset_deck(self)
        self.assertEqual(game.deck.len_card(), 52)

    def test_players_init_setting(self):
        game = Game([Player("Player"), Computer("Computer")])
        game.deal_cards()
        self.assertEqual(len(game.players[0].cards), 7)

    # 카드 덱에서 처음 open된 카드가 존재 하는지 
    def test_openned_card(self):
        game = Game([Player("Player"), Computer("Computer")])
        game.deal_cards()
        self.assertEqual(0, game.current_player_index)
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        
        # 덱의 첫 번째 카드가 존재 하는지 
        color_type = ["red", "blue", "green", "yellow", "black"]
        self.assertIn(gamePage.game.deck.pop_card().color, color_type)

    #deck 클릭 했을 때 추가 잘 되었는지 and 턴 잘 넘어갔는지 
    def test_deck_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        deck_rect = gamePage.draw_deck()
        card_rect_list = gamePage.display_player_cards()

        gamePage.flip_deck_card(True)

        self.assertEqual(7, len(gamePage.game.players[0].cards))

        # 클릭 
        gamePage.process_deck_clicked(deck_rect, card_rect_list[0])

        self.assertEqual(8, len(gamePage.game.players[0].cards))

        self.assertEqual(1, gamePage.game.current_player_index)

    # 내 덱에 있는 카드 내는 경우 
    def test_my_deck_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        deck_rect = gamePage.draw_deck()
        card_rect_list = gamePage.display_player_cards()

        gamePage.handle_card_hover(screen, card_rect_list, gamePage.screen_height)

    # 기능 카드 plus_4
    def test_plus4_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.pick_current_card()

        gamePage.game.plus4_card_clicked(gamePage.game.players[0], "black")

        self.assertEquals(11, len(gamePage.game.players[1].cards))

    # 기능 카드 plus_2
    def test_plus2_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.pick_current_card()
        
        gamePage.game.plus2_card_clicked(gamePage.game.players[0])

        self.assertEqual(9, len(gamePage.game.players[1].cards))

    # 기능 카드 skip
    def test_skip_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.pick_current_card()
        
        gamePage.game.skip_card_clicked()

        self.assertEqual(0, gamePage.game.current_player_index)

    # 기능 카드 reverse
    def test_reverse_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.pick_current_card()
        
        gamePage.game.reverse_card_clicked()

        self.assertEqual(-1, gamePage.game.direction)
    # 기능 카드 change_all 
    def test_change_all_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.pick_current_card()

        
        first_card = gamePage.game.players[0].cards[0]

        # 카드 배열의 첫번째 인덱스 비교 
        gamePage.game.change_all_clicked(1, "black")

        second_card = gamePage.game.players[1].cards[0]

        self.assertEqual(first_card, second_card)

    # 기능 카드 wildcard
    def test_wild_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()
        gamePage.game.pick_current_card()


        gamePage.game.wildcard_card_clicked("black")
    
        self.assertEqual("black", gamePage.game.current_card.color)

    # 기능 카드 bombcard (자신 외 전체 3장씩 추가)
    def test_bombcard_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.players.append(Computer("COMPUTER 1"))
        gamePage.game.deal_cards()
        gamePage.game.pick_current_card()

        gamePage.game.bombcard_card_clicked("black")
        
        self.assertEqual("black", gamePage.game.current_card.color)
        self.assertEqual(10, len(gamePage.game.players[1].cards))
        self.assertEqual(10, len(gamePage.game.players[2].cards))

    # UNO 버튼 클릭 했을 경우 
    def test_uno_button_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        # 자신의 덱에 카드가 한 장이 아닐 때 
        res = gamePage.game.uno_button_clicked(0)
        self.assertEqual(False, res)

        # 자신의 덱에 카드가 한 장일 때 (위에서 +1 해서 8장임)
        for _ in range(7): 
            del gamePage.game.players[0].cards[0]
        
        res = gamePage.game.uno_button_clicked(0)
        
        self.assertEqual(True, res)
            
    # 드로우 버튼 클릭 했을 경우
    def test_draw_card_clicked(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        gamePage.game.draw_card_clicked(gamePage.game.players[0])

        self.assertEqual(8, len(gamePage.game.players[0].cards))
    
    # 자신의 덱 0장 되었을 때 game_win
    def test_game_win(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        for _ in range(7):
            del gamePage.game.players[0].cards[0]
 
        res = gamePage.game.game_win(gamePage.game.players[0])

        self.assertTrue(True, res)
    
    # pickle 사용 되는지 
    def test_use_pickle(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)
        gamePage.game.deal_cards()

        obj = len(gamePage.game.players[0].cards)
        data = pickle.dumps(obj)
        
        self.assertEqual(obj, pickle.loads(data))
    
    # 카드 덱이 모두 소진 됐을 때 
    def test_game_deck_all_used(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)

        gamePage.game.reset_deck()

        for _ in range(52):
            gamePage.game.deck.pop_card()        
        
        # self.assertEqual(0, gamePage.game.deck.len_card())
        # 현재 덱에 존재하는 카드 0개 
        mock_event = MagicMock(type = pygame.KEYDOWN, key=pygame.K_ESCAPE)

        res = gamePage.game_deck_used_all(mock_event)

        self.assertEqual("pause", res)
    
    

if __name__ == '__main__':
    unittest.main()
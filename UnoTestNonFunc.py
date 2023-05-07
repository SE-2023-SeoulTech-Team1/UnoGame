import time
import unittest
from GamePage import *
from Setting import *
from Game import *

class non_func_test(unittest.TestCase):
        
    def test_draw_card_performance(self):
        setting = Setting()
        screen = pygame.display.set_mode(setting.screen_size)
        gamePage = GamePage(screen, setting)

        gamePage.game.reset_deck()

        start_time = time.time()

        deck = gamePage.game.deck

        for i in range(50):
            deck.pop_card()

        end_time = time.time()
            
        duration = end_time - start_time

        assert duration < 1.0, f"Test failed: {duration:.2f} seconds"
        


if __name__ == '__main__':
    unittest.main()



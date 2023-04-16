import pygame

TIMEOUT = 10

class Timer:
    def __init__(self, game_page):
        self.timer_flag = True
        self.start_ticks = None
        self.count = True
        self.deck_cards_num = len(game_page.game.deck.cards)
        self.player_cards_num = len(game_page.game.players[0].cards)
        self.game_page = game_page
        self.game = game_page.game

    # def start(self):
        if self.count is True:
            self.start_ticks = pygame.time.get_ticks()
            print(f"\n현재 {self.game.players[self.game.current_player_index].name}의 턴입니다.")
            deck_cards_num = len(self.game.deck.cards)
            player_cards_num = len(self.game.players[0].cards)
            self.count = False

    def run(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if TIMEOUT - elapsed_time > 0 \
                and self.deck_cards_num == len(self.game.deck.cards) \
                and self.player_cards_num == len(self.game.players[0].cards):
            elapsed_time = (pygame.time.get_ticks() - startTicks) / 1000
            timer = font.render(str(int(totalTime - elapsed_time)), True, WHITE)
            self.game_page.screen.blit(timer, (20, 20))
            self.game_page.who_is_current_player()

        # if setTimer == True:
        #     elapsed_time = (pygame.time.get_ticks() - startTicks) / 1000
        #     if totalTime - elapsed_time > 0 and deck_cards_num == len(self.game.deck.cards) and player_cards_num == len(
        #             self.game.players[0].cards):
        #         elapsed_time = (pygame.time.get_ticks() - startTicks) / 1000
        #         timer = font.render(str(int(totalTime - elapsed_time)), True, WHITE)
        #         screen.blit(timer, (20, 20))
        #         self.who_is_current_player()
        #     elif deck_cards_num != len(self.game.deck.cards) or player_cards_num != len(self.game.players[0].cards):
        #         setTimer = False
        #         timerFlag = False
        #         count = True
        #         # 여기서 next_turn 안하고 카드들 선택한다음 그곳에서 next_turn하는 방식으로 바꿈
        #         # game.next_turn()
        #     elif totalTime - elapsed_time > -1:
        #         timeout = font.render("TIME OUT", True, WHITE)
        #         screen.blit(timeout, (20, 20))
        #         self.who_is_current_player()
        #     else:
        #         setTimer = False
        #         timerFlag = False
        #         count = True
        #         print("\n제한시간이 지났습니다. 상대 턴입니다.")
        #         # 다음 플레이어로 넘어가기
        #         self.game.next_turn()



    # def timer(self, setTimer, totalTime):
    #     global timerFlag, startTicks, count, deck_cards_num, player_cards_num
    #
    #     # timer 최초 호출
    #     if self.count is True:
    #         startTicks = pygame.time.get_ticks()
    #         print(f"\n현재 {self.game.players[self.game.current_player_index].name}의 턴입니다.")
    #         deck_cards_num = len(self.game.deck.cards)
    #         player_cards_num = len(self.game.players[0].cards)
    #         self.count = False
    #
    #     # timer 실행
    #     if setTimer == True:
    #         elapsed_time = (pygame.time.get_ticks()-startTicks) / 1000
    #         if totalTime - elapsed_time > 0 and deck_cards_num == len(self.game.deck.cards) and player_cards_num == len(self.game.players[0].cards):
    #             elapsed_time = (pygame.time.get_ticks()-startTicks) / 1000
    #             timer = font.render(str(int(totalTime - elapsed_time)), True, WHITE)
    #             screen.blit(timer, (20, 20))
    #             self.who_is_current_player()
    #         elif deck_cards_num != len(self.game.deck.cards) or player_cards_num != len(self.game.players[0].cards):
    #             setTimer = False
    #             timerFlag = False
    #             count = True
    #             # 여기서 next_turn 안하고 카드들 선택한다음 그곳에서 next_turn하는 방식으로 바꿈
    #             # game.next_turn()
    #         elif totalTime - elapsed_time > -1:
    #             timeout = font.render("TIME OUT", True, WHITE)
    #             screen.blit(timeout, (20, 20))
    #             self.who_is_current_player()
    #         else:
    #             setTimer = False
    #             timerFlag = False
    #             count = True
    #             print("\n제한시간이 지났습니다. 상대 턴입니다.")
    #             # 다음 플레이어로 넘어가기
    #             self.game.next_turn()
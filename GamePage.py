import pygame
from Game import *
from animate import *
from draw import *
from handle_card_hover import *


class GamePage():
    def __init__(self, screen, setting, player_names):
        self.screen = screen
        self.setting = setting
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.game = Game(player_names)
        self.clock = pygame.time.Clock()

        self.card_move_sound = pygame.mixer.Sound(resource_path('./assets/cardmove.mp3'))
        self.card_select_sound = pygame.mixer.Sound(resource_path('./assets/cardclick.mp3'))

        # TODO timer는 턴이 바뀔 때마다 새로운 객체 생성 후 실행

    def running(self):
        self.clock.tick(60)

        # 카드 초기 세팅
        self.game.deal_cards()

        pygame.mixer.music.load(resource_path('./assets/background.mp3'))
        # pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(self.setting.volume * 0.01 * self.setting.back_volume * 0.01)

        running = True

        draw_game_screen(self)
        self.game.deck.draw(self)
        for i, card in enumerate(self.game.players[0].cards):
            card.draw_front(self.screen, 0.1 + 0.05 * i, 0.85)
        flip_deck_card(self)
        draw_current_card(self)

        while running:
            draw_game_screen(self)
            handle_card_hover(self)
            # handle_card_clicked(self)
            draw_current_card(self)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                # TODO Keyboard operation
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass
                    elif event.key == pygame.K_BACKSPACE:
                        pass
                    elif event.unicode.isprintable():
                        pass

            # Update
            # self.game.update()

            # pygame.display.update()
            # pygame.time.Clock().tick(self.setting.fps)



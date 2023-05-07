import pygame.mouse
from draw import draw_game_screen


def handle_card_hover(game_page):

    for i, card in enumerate(game_page.game.players[0].cards):
        mouse_pos = pygame.mouse.get_pos()

        if card.rect.collidepoint(mouse_pos):
            card.y = 0.8
            pygame.display.flip()
        else:
            card.y = 0.85
            pygame.display.flip()

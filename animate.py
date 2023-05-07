import os
import pygame
from draw import *


def flip_deck_card(game_page):
    screen_width, screen_height = pygame.display.get_surface().get_size()

    game_page.card_move_sound.play()
    game_page.card_move_sound.set_volume(game_page.setting.volume * 0.01 * game_page.setting.effect_volume * 0.01)

    flip_card = game_page.game.pick_current_card()
    x, y = screen_width * 0.25, screen_height * 0.25
    target_x, target_y = screen_width * 0.4, screen_height * 0.25
    flip_card.move(game_page, x, y, target_x, target_y, speed=7)

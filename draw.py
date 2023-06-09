import pygame
from resource_path import *

pygame.init()

# 색상 정의
DARKGREEN = (8, 44, 15)
GREY = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (185, 52, 31)
BLUE = (0, 0, 255)
GREEN = (0, 143, 0)
YELLOW = (255, 218, 71)
BLACK = (0, 0, 0)

SELECT_COLOR = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW}

# 폰트 설정
font = pygame.font.SysFont(None, 30)
unoFont = pygame.font.SysFont(None, 40)

# 기본 배경 설정
backgroundColor = DARKGREEN

def cardFrontImg(color, type):
    return pygame.image.load(resource_path('./assets/cards/' + color + type + '.png')).convert_alpha()


def draw_card_front(screens, card, top, left):
    card_front_img = pygame.image.load(card.front).convert_alpha()
    screens.blit(card_front_img, (left, top))


def draw_card_back(screens, card, top, left):
    card_back_img = pygame.image.load(card.back).convert_alpha()
    screens.blit(card_back_img, (left, top))


def draw_computer_player_names(game_page):
    for computer_player_text in game_page.computer_players_names:
        computer_player_text.render(game_page.screen)

def draw_game_screen(game_page):
    player_bg_x = game_page.screen.get_width()*0.75
    player_bg_width = game_page.screen.get_width()*0.25
    # 배경 색 설정/추후 배경사진 추가
    game_page.screen.fill(backgroundColor)
    draw_computer_player_names(game_page)

    # 현재 방향 아이콘 표시
    if game_page.game.direction == 1:
        direction_icon = pygame.image.load(resource_path("./assets/clockwise.png"))
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))

    else:
        direction_icon = pygame.image.load(resource_path("./assets/counterclockwise.png"))
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))
    game_page.screen.blit(direction_icon, (game_page.screen.get_width() * 0.06, game_page.screen.get_height() * 0.025))

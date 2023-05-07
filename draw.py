from resource_path import *
from Text import *
from Button import *

SELECT_COLOR = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW}


def cardFrontImg(color, type):
    return pygame.image.load(resource_path('./assets/cards/' + color + type + '.png')).convert_alpha()


def draw_card_front(screen, card, top, left, scale=1):
    card_front_img = card.front_img
    card_front_img = pygame.transform.scale(
        card_front_img, (card_front_img.get_rect().size[0] * scale, card_front_img.get_rect().size[1] * scale))
    screen.blit(card_front_img, (left, top))


def draw_card_back(screen, card, top, left, scale):
    card_back_img = pygame.image.load(card.back).convert_alpha()
    card_back_img = pygame.transform.scale(
        card_back_img, (card_back_img.get_rect().size[0] * scale, card_back_img.get_rect().size[1] * scale))
    screen.blit(card_back_img, (left, top))


def draw_computer_player_names(game_page):
    for i, computer_player in enumerate(game_page.game.computer_players):
        Text(x=0.8,
             y=0.2 * i + 0.07,
             text=f"{computer_player.name}",
             color=WHITE,
             size=20).render(game_page.screen)


def draw_current_player_name(game_page):
    Text(x=0.75 * 0.5,
         y=0.05,
         text=f"{game_page.game.players[game_page.game.current_player_index].name}",
         color=WHITE,
         size=20).render(game_page.screen)


def draw_direction(game_page):
    if game_page.game.direction == 1:
        direction_icon = pygame.image.load(resource_path("./assets/clockwise.png"))
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))
    else:
        direction_icon = pygame.image.load(resource_path("./assets/counterclockwise.png"))
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))
    game_page.screen.blit(direction_icon, (game_page.screen.get_width() * 0.06, game_page.screen.get_height() * 0.025))


def draw_computer_cards(game_page):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    computer_players = game_page.game.computer_players
    for player_idx, computer_player in enumerate(computer_players):
        for card_idx, card in enumerate(computer_player.cards):
            draw_card_back(game_page.screen, card, screen_height * (0.2 * player_idx + 0.1), screen_width * 0.92 - card_idx * 20, 0.7)


def draw_player_cards(game_page):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    for i, card in enumerate(game_page.game.players[0].cards):
        card.draw_front(game_page.screen, 0.1 + 0.05 * i, 0.85)


def draw_current_card(game_page):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    card = game_page.game.current_card
    if card:
        draw_card_front(game_page.screen, card, screen_height * 0.25, screen_width * 0.4)


def draw_game_screen(game_page):
    game_page.screen.fill(DARKGREEN)
    draw_computer_player_names(game_page)
    draw_current_player_name(game_page)
    draw_direction(game_page)
    game_page.game.deck.draw(game_page)
    for i, card in enumerate(game_page.game.players[0].cards):
        card.draw_front(game_page.screen, card.x, card.y)
    draw_computer_cards(game_page)
    draw_current_card(game_page)


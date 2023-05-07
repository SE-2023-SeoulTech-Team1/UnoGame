import pygame
from draw import *
from resource_path import *

COLORS = ['red', 'yellow', 'green', 'blue']
ALL_COLORS = COLORS + ['black']
NUMBERS = list(range(1, 10))
SPECIAL_CARD_TYPES = ['skip', 'reverse', '+2']
COLOR_CARD_TYPES = NUMBERS + SPECIAL_CARD_TYPES
BLACK_CARD_TYPES = ['wildcard', '+4', 'bomb', 'all']
ALL_TYPES = NUMBERS + SPECIAL_CARD_TYPES + BLACK_CARD_TYPES

class Card:
    def __init__(self, color, type, color_weak_mode=False):
        if color not in ALL_COLORS:
            print("Invalid Card Color.")
            exit(-1)
        if type not in ALL_TYPES:
            print("Invalid Card Type")
            exit(-1)

        self.color = color
        self.type = type
        if color_weak_mode:
            self.front = resource_path(f"./assets/colorWeakCards/{self.color}{self.type}.png")
            self.back = resource_path("./assets/colorWeakCards/unoCardBack.png")
        else:
            self.front = resource_path(f"./assets/cards/{self.color}{self.type}.png")
            self.back = resource_path("./assets/cards/unoCardBack.png")
        self.front_img = pygame.image.load(self.front).convert_alpha()
        self.back_img = pygame.image.load(self.back).convert_alpha()
        self.rect = pygame.image.load(self.front).convert_alpha().get_rect()
        self.x, self.y = self.rect.center

    def __str__(self):
        return f'Uno Card Object: {self.color} {self.type}'


    def draw_front(self, screen, x, y):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x, self.y = x, y
        self.rect.center = screen_width * self.x, screen_height * self.y
        screen.blit(self.front_img, (self.rect.left, self.rect.top))

    def draw_back(self, screen, x, y):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x, self.y = x, y
        self.rect.center = screen_width * self.x, screen_height * self.y
        screen.blit(self.back_img, self.rect.center)

    def hover(self, screen):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.y = 0.8
        # self.draw_front(screen, self.x, self.y)

    def move(self, screen, x, y, target_x, target_y, speed):

        # Start the loop
        done = False
        while not done:

            # Calculate the distance between the current position and the target position
            distance_x = target_x - x
            distance_y = target_y - y

            # Calculate the direction of the movement
            direction_x = 1 if distance_x > 0 else 0
            direction_y = 1 if distance_y > 0 else 0

            # Calculate the amount to move in each direction
            move_x = speed * direction_x
            move_y = speed * direction_y

            # Update the position of the image
            if x + move_x > target_x:
                x = target_x
            else:
                x += move_x

            if y + move_y > target_y:
                y = target_y
            else:
                y += move_y

            # Draw the image on the screen
            screen.screen.blit(self.front_img, (x, y))

            # Update the screen
            pygame.display.update()
            draw_game_screen(screen)

            # Check if the target position has been reached
            if (x == target_x or x < 0) and y == target_y:
                done = True
                screen.screen.blit(self.front_img, (x, y))
                pygame.display.update()
                return target_x, target_y

class Deck:
    def __init__(self, cards):
        if len(cards) < 1:
            print("At least one more cards should be in deck.")
            exit(-1)
        self.cards = cards
        self.rect = None

    def len_card(self):
        return len(self.cards)

    def pop_card(self):
        return self.cards.pop()


    def draw(self, screen):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        for i, card in enumerate(self.cards):
            top = screen_height * 0.25 - i / 10
            left = screen_width * 0.25 - i / 10
            screen.screen.blit(card.back_img, (left, top))

        if len(self.cards) != 0:
            self.rect = pygame.Rect(left, top, card.back_img.get_width(),
                            card.back_img.get_height())

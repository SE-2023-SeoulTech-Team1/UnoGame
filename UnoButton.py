import pygame

class UnoButton:
    def __init__(self, game_page):
        self.game_page = game_page
        self.game = game_page.game
        self.img = pygame.image.load('./assets/unobutton.png').convert_alpha()
        self.rect = self.img.get_rect()


    def draw(self):
        # self.rect.centerx = round(boardx + boardWidth * 0.5)
        # self.rect.y = screenHeight * 0.45

        screen_width, screen_height = self.game_page.screen.get_size()

        self.rect.centerx = screen_width * 0.35
        self.rect.y = screen_height * 0.45
        self.game_page.screen.blit(self.img, self.rect)

    def clicked(self, player_idx):
        player_with_one_card = [player for player in self.game.players if len(player.cards) == 1]
        if not player_with_one_card:
            self.game.players[player_idx].draw_card(self.game.deck)
            return False

        if len(self.game.players[player_idx].cards) == 1:
            self.game.uno = player_idx
        else:
            for player in player_with_one_card:
                player.draw_card(self.game.deck)
        return True

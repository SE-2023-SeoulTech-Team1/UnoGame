import pygame
from Colors import *
from Button import Button, TextButton
from Text import *

class LobbyPage():
    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting

        self.btn_player = TextButton(0.5, 0.1, 200, 50, "Your name")
        self.btn_computer_players = [TextButton(0.5, 0.1 * (i + 1) + 0.15, 200, 50, "") for i in range(5)]
        self.btn_start = Button(0.5, 0.8, 200, 50, "Start Game")

    def running(self):
        selected_idx = None
        player_selected = [False for _ in range(5)]

        while True:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_player.rect.collidepoint(event.pos):
                        selected_idx = -1

                    for i, btn in enumerate(self.btn_computer_players):
                        if btn.rect.collidepoint(event.pos):
                            if player_selected[i]:
                                player_selected[i] = False
                                self.btn_computer_players[i].text = ""
                                selected_idx = None
                            else:
                                player_selected[i] = True
                                selected_idx = i

                    # When Start button clicked
                    if self.btn_start.rect.collidepoint(event.pos):
                        if player_selected.count(True) == 0:
                            pass
                        else:
                            player_names = [self.btn_player.text] + [self.btn_computer_players[i].text for i in range(5) if player_selected[i]]
                            return "game", player_names

                elif event.type == pygame.KEYDOWN and selected_idx is not None:
                    if event.key == pygame.K_RETURN:
                        pass
                    if event.key == pygame.K_BACKSPACE:
                        if selected_idx == -1:
                            self.btn_player.text = self.btn_player.text[:-1]
                        elif selected_idx > -1:
                            self.btn_computer_players[selected_idx].text = self.btn_computer_players[selected_idx].text[:-1]
                    elif event.unicode.isprintable():
                        if selected_idx == -1:
                            self.btn_player.text += event.unicode
                        elif selected_idx > -1:
                            self.btn_computer_players[selected_idx].text += event.unicode

            # draw the background
            self.screen.fill(WHITE)

            # processing computer player buttons
            for i, btn in enumerate(self.btn_computer_players):
                btn.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, btn.rect, 2)
                if player_selected[i]:
                    center = (btn.top - self.screen.get_width() * 0.03, btn.left + btn.height // 2)
                    pygame.draw.circle(self.screen, NEON_GREEN, center, radius=7)

            # processing player button
            self.btn_player.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_player, 2)

            # processing start button
            self.btn_start.process(self.screen)

            # Update the display
            pygame.display.update()

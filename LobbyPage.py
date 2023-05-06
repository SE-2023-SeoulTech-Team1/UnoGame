import pygame
from Colors import *
from Button import Button, TextButton
from Text import *

class LobbyPage():
    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting

        self.player
        self.btn_players = [TextButton(0.5, 0.1 * (i + 1) + 0.1, 200, 50, "") for i in range(5)]
        self.btn_start = Button(0.5, 0.8, 200, 50, "Start Game")

# 클릭되어있는지 안되어있는지 상태 저장하는 자료구조 있어야 함
    def set_game_players(self):
        return None


    def running(self):
        selected_idx = 0
        player_selected = [False for _ in range(5)]

        while True:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, btn in enumerate(self.btn_players):
                        if btn.rect.collidepoint(event.pos):
                            if player_selected[i]:
                                player_selected[i] = False
                                self.btn_players[i].text = ""
                            else:
                                player_selected[i] = True
                                selected_idx = i
                                btn.surface.fill(PINK)
                            selected_idx = i

                    # When Start button clicked
                    if self.btn_start.rect.collidepoint(event.pos):
                        return set_game_players()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass
                    if event.key == pygame.K_BACKSPACE:
                        self.btn_players[selected_idx].text = self.btn_players[selected_idx].text[:-1]
                    elif event.unicode.isprintable():
                        self.btn_players[selected_idx].text += event.unicode

            # Draw the game screen
            self.screen.fill((255, 255, 255))
            for i, btn in enumerate(self.btn_players):
                btn.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, btn.rect, 2)
                if player_selected[i] == True:
                    center = (btn.top - self.screen.get_width() * 0.03, btn.left + btn.height // 2)
                    pygame.draw.circle(self.screen, NEON_GREEN, center, radius=7)
            self.btn_start.process(self.screen)

            # Update the display
            pygame.display.update()
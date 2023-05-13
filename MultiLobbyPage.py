import pygame
from Colors import *
from Button import Button, TextButton, Reverse_TextButton
from Text import *
import socket
import threading
from multigame.Client import Client
from multigame.Server import Server


class MultiLobbyPage():
    def __init__(self, screen, setting, is_host = False):
        self.screen = screen
        self.setting = setting
        self.is_host = is_host
        self.server = None
        self.client = None
        self.btn_server = TextButton(0.5, 0.1, 200, 50, "Server")
        self.btn_clients = [Reverse_TextButton(0.5, 0.1 * (i + 1) + 0.15, 200, 50, "") for i in range(5)]
        self.btn_start = Button(0.5, 0.8, 200, 50, "Start Game")
        self.thread = threading.Thread(target=self.run_server_or_client)
        self.thread.daemon = True
        print("상태 : " + str(is_host))
        self.player_selected = [False for _ in range(5)]
        self.player_names = []
        self.multi_lobby_page = self

        self.thread.start()

    def run_server_or_client(self):
        if self.is_host:
            self.server = Server(self.multi_lobby_page)
            self.server.run()
        else:
            self.client = Client(self.multi_lobby_page)

    def running(self):
        # initialize pygame
        pygame.init()

        selected_idx = None

        while True:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_server.rect.collidepoint(event.pos):
                        selected_idx = -1

                    for i, btn in enumerate(self.btn_clients):
                        if btn.rect.collidepoint(event.pos):
                            if self.player_selected[i]:
                                self.player_selected[i] = False
                                self.btn_clients[i].text = ""
                                selected_idx = None
                            
                            else:
                                self.player_selected[i] = True
                                selected_idx = i
                            print(self.client)
                    # When Start button clicked
                    if self.btn_start.rect.collidepoint(event.pos):
                        if self.player_selected.count(True) == 0:
                            pass
                        else:
                            player_names = [self.btn_server.text] + [self.btn_clients[i].text for i in range(5) if self.player_selected[i]]
                            return "game", player_names

                elif event.type == pygame.KEYDOWN and selected_idx is not None:
                    if event.key == pygame.K_RETURN:
                        pass
                    if event.key == pygame.K_BACKSPACE:
                        if selected_idx == -1:
                            self.btn_server.text = self.btn_server.text[:-1]
                        elif selected_idx > -1:
                            self.btn_clients[selected_idx].text = self.btn_clients[selected_idx].text[:-1]
                    elif event.unicode.isprintable():
                        if selected_idx == -1:
                            self.btn_server.text += event.unicode
                        elif selected_idx > -1:
                            self.btn_clients[selected_idx].text += event.unicode

            # draw the background
            self.screen.fill(WHITE)

            # processing computer player buttons
            for i, btn in enumerate(self.btn_clients):
                btn.process(self.screen, self.player_selected[i])
                pygame.draw.rect(self.screen, BLACK, btn.rect, 2)

            # processing player button  
            self.btn_server.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_server, 2)

            # processing start button
            self.btn_start.process(self.screen)

            # Update the display
            pygame.display.update()


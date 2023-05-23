import pygame
from Colors import *
from Button import Button, TextButton, Reverse_TextButton
from Text import *
import threading
from multigame.Client import Client
from multigame.Server import Server


class MultiLobbyPage():
    def __init__(self, screen, setting, multi_setting_page = None, is_host = False):
        self.screen = screen
        self.setting = setting
        self.client = None
        self.server = None
        self.is_host = is_host
        self.multi_setting_page = multi_setting_page
        self.multi_lobby_page = self
        self.btn_server = TextButton(0.5, 0.1, 200, 50, "Server")
        self.btn_clients = [Reverse_TextButton(0.5, 0.1 * (i + 1) + 0.15, 200, 50, "") for i in range(5)]
        self.btn_start = Button(0.5, 0.8, 200, 50, "Start Game")
        self.btn_ip = TextButton(0.5, 0.9, 150, 25, "")
        self.player_selected = [False for _ in range(5)]
        self.thread = threading.Thread(target=self.running_server).start()
        self.player_names = []
        self.client_data = {}   
        self.enter_client = False
        self.update_client = True
        self.run_server = False
        self.thread = None
        self.update_lobby_page = False
        self.client_num = 0
        self.text_error = Text(0.35, 0.15, "More than 5 people", RED)
        self.over_five = False
        
        
    def running_server(self):
        if self.is_host:
            self.server = Server(self.multi_lobby_page)    

    def running(self):
        # initialize pygame
        pygame.init()

        selected_idx = None

        while True:

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.multi_setting_page.client.disconnect()
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

            # processing if client enter lobby
            self.enter_lobby()
            self.update_lobby()

            # processing computer player buttons
            for i, btn in enumerate(self.btn_clients):
                btn.process(self.screen, self.player_selected[i])
                pygame.draw.rect(self.screen, BLACK, btn.rect, 2)

            # processing player button  
            self.btn_server.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_server, 2)

            # processing start button
            self.btn_start.process(self.screen)


            self.btn_ip.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_ip, 2)


            if self.over_five:
                self.text_error.render(self.screen)

            # Update the display
            pygame.display.update()

    def enter_lobby(self):
        # 클라이언트가 방에 들어왔다고 서버에 전송 
        if self.enter_client:
            self.multi_setting_page.client.send_data("enter_lobby")
            self.enter_client = False
    
    def update_lobby(self):
        if self.update_lobby_page:
            for i, player in enumerate(self.client_data['player_selected']):
                if player:
                    self.player_selected[i] = player
                    if i < len(self.client_data['clients']):
                        self.multi_lobby_page.btn_clients[i].text = self.client_data['clients'][i]['name']
                    
            self.update_lobby_page = False
            # 클라이언트 숫자만큼 



            

from Button import Button, TextButton
from Colors import *
from multigame.Client import Client
from MultiLobbyPage import MultiLobbyPage
import threading
import json
import pickle

class MultiSettingPage():
    def __init__(self, screen, setting):
        self.screen = screen
        self.setting = setting
        self.correct_ip = False
        self.correct_pwd = False
        self.thread_running = 0
        self.thread = None
        self.data = {}
        self.client = None
        self.multi_setting_page = self
        self.btn_ip = TextButton(0.5, 0.1, 200, 50, "IP Adress")
        self.btn_input_ip = TextButton(0.5, 0.2, 200, 50, "")
        self.btn_submit_ip = Button(0.5, 0.3, 200, 50, "Submit")
        self.btn_name = TextButton(0.5, 0.4, 200, 50, "Name")
        self.btn_input_name = TextButton(0.5, 0.5, 200, 50, "")
        self.btn_pwd = TextButton(0.5, 0.6, 200, 50, "Password")
        self.btn_input_pwd = TextButton(0.5, 0.7, 200, 50, "")
        self.btn_submit_pwd = Button(0.5, 0.8, 200, 50, "Submit")
        self.enter = False
        self.multi_lobby_page = MultiLobbyPage(screen, setting, self.multi_setting_page)


    def running(self):
        selected_idx = None    

        while True:
            self.screen.fill(WHITE)

            if self.thread_running == 1 and self.client is None:
                self.client = Client(self)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btn_input_ip.rect.collidepoint(event.pos):
                        selected_idx = -1 if selected_idx != -1 else 1
                    
                    if self.btn_input_name.rect.collidepoint(event.pos):
                        selected_idx = -2 if selected_idx != -2 else 2

                    if self.btn_input_pwd.rect.collidepoint(event.pos):
                        selected_idx = -3 if selected_idx != -3 else 3

                    if self.btn_submit_ip.rect.collidepoint(event.pos):
                        if self.btn_input_ip.text is not "":
                            client = self.btn_input_ip.text
                            self.compare_ip(0, "127.0.0.1", client)

                    if self.btn_submit_pwd.rect.collidepoint(event.pos):
                        if self.btn_input_pwd.text is not "":
                            pwd = self.btn_input_pwd.text
                            name = self.btn_input_name.text
                            self.data['pwd'] = pwd
                            self.data['name'] = name
                            json_data = json.dumps(self.data)
                            self.client.send_data(json_data)
                            self.client.name = name
                        
                elif event.type == pygame.KEYDOWN and selected_idx is not None:
                    if event.key == pygame.K_BACKSPACE:
                        if selected_idx == -1:
                                self.btn_input_ip.text = self.btn_input_ip.text[:-1]
                        if selected_idx == -2:
                                self.btn_input_name.text = self.btn_input_name.text[:-1]
                        if selected_idx == -3:
                                self.btn_input_pwd.text = self.btn_input_pwd.text[:-1]
                    elif event.unicode.isprintable():
                        if selected_idx == -1:
                            self.btn_input_ip.text += event.unicode
                        if selected_idx == -2:
                            self.btn_input_name.text += event.unicode 
                        if selected_idx == -3:
                            self.btn_input_pwd.text += event.unicode 
            
            if selected_idx == -1:
                center = (self.btn_input_ip.top - self.screen.get_width() * 0.03, self.btn_input_ip.left + self.btn_input_ip.height // 2)
                pygame.draw.circle(self.screen, NEON_GREEN, center, radius=7)
            if selected_idx == -2:
                center = (self.btn_input_name.top - self.screen.get_width() * 0.03, self.btn_input_name.left + self.btn_input_name.height // 2)
                pygame.draw.circle(self.screen, NEON_GREEN, center, radius=7)
            if selected_idx == -3:
                center = (self.btn_input_pwd.top - self.screen.get_width() * 0.03, self.btn_input_pwd.left + self.btn_input_pwd.height // 2)
                pygame.draw.circle(self.screen, NEON_GREEN, center, radius=7)

            
            self.btn_ip.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_ip.rect, 2)
            self.btn_input_ip.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_input_ip.rect, 2)
            self.btn_submit_ip.process(self.screen)
            pygame.draw.rect(self.screen, BLACK, self.btn_submit_ip.rect, 2)

            if self.correct_ip == True:
                self.btn_name.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, self.btn_name.rect, 2)
                self.btn_input_name.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, self.btn_input_name.rect, 2)
                self.btn_pwd.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, self.btn_pwd.rect, 2)
                self.btn_input_pwd.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, self.btn_input_pwd.rect, 2)
                self.btn_submit_pwd.process(self.screen)
                pygame.draw.rect(self.screen, BLACK, self.btn_submit_pwd.rect, 2)
                self.thread_running += 1

            if self.enter == True:
                # 방에 접속 
                self.multi_lobby_page.client = self.client
                self.multi_lobby_page.enter_client = True
                self.client.multi_lobby_page = self.multi_lobby_page
                return "multi_lobby", self.multi_lobby_page

            pygame.display.update()
    
    def compare_ip(self, i, server, client):
        if i == 0:
            self.correct_ip = server == client

        if i == 1:
            self.correct_pwd = server == client
    

            






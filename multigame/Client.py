import socket
import threading

class Client:
    def __init__(self, multi_lobby_page):
        self.host = "localhost"
        self.port = 12345
        self.name = "Player"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.multi_lobby_page = multi_lobby_page
        try:
            self.socket.connect((self.host, self.port))
        except:
            print("Connection failed.")
            return
        self.name = input("이름을 입력하세요 : ")
        self.send_data(self.name)
        self.receive_data()



    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                print(data)
                if data:
                    commands = data.split('|n')
                    for command in commands:
                        parts = command.split(',')
                        if parts[0] == 'update':
                            for i, part in enumerate(parts[1:]):
                                self.multi_lobby_page.player_selected[i] = part == 'True'
                        elif parts[0] == 'update_btn_text':
                            for i, part in enumerate(parts[1:]):
                                self.multi_lobby_page.btn_clients[i].text = part

                    


            except:
                break


    def send_data(self, data):
        self.socket.sendall(data.encode())



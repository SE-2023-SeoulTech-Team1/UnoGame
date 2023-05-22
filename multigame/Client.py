import socket
import threading
import json
import pickle

class Client:
    def __init__(self, multi_setting_page = None, multi_lobby_page = None, ip_address = None):
        self.host = ip_address
        self.port = 12345
        self.name = "Player"
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.multi_setting_page = multi_setting_page
        self.multi_lobby_page = multi_lobby_page
        self.data = {}
        self.my_data = {}
        try:
            self.socket.connect((self.host, self.port))
        except:
            print("Connection failed.")
            return
        self.name = "hi"
        self.send_data(self.name)
        threading.Thread(target=self.receive_data).start()
        
        
    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data: 
                    pass
                json_data = data
                message = json.loads(json_data)

                self.data = message

                for client in self.data['clients']:
                    if client.get('enter_lobby'):
                        name = client.get('name')
                        if name == self.name:
                            self.my_data = client
                            #multi_lobby_page에 접속 하도록 
                            self.multi_setting_page.enter = True
                    else:
                        self.multi_setting_page.over_five = True
                break
            except:
                print("client error!")
                break

        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data: 
                    pass
                json_data = data
                message = json.loads(json_data)
                print(message)
                self.multi_lobby_page.client_data = message

                self.multi_lobby_page.update_lobby_page = True
                
            except:
                break
    def send_data(self, data):
        self.socket.sendall(data.encode())
    

    def disconnect(self):
        self.socket.close()

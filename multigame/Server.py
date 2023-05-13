import socket
import threading

class Server:
    def __init__(self, multi_lobby_page):
        self.host = ''
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.clients = []
        self.multi_lobby_page = multi_lobby_page

    def handle_client(self, client_socket, client_address):
        print(f'New client connected: {client_address}')
        name = client_socket.recv(1024).decode()
        print(f'{name} has connected.')

        for i, player in enumerate(self.multi_lobby_page.player_selected):
            if player and self.multi_lobby_page.btn_clients[i].text is "":
                self.multi_lobby_page.btn_clients[i].text = name
                break
        
        for c in self.clients:
            c.sendall(f'update,{",".join(str(p) for p in self.multi_lobby_page.player_selected)}'.encode() + b'|n')
            c.sendall(f'update_btn_text,{",".join(self.multi_lobby_page.btn_clients[i].text for i in range(5))}'.encode() + b'|n')

        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                
                # handle received data here
                print(data)
            except:
                print(f'Client {name} has disconnected.')

                # reset client's selected player data
                for i, text in enumerate(self.multi_lobby_page.btn_clients):
                    if text == name:
                        self.multi_lobby_page.btn_clients[i].text = ""
                        break

                # update all clients with updated button text
                for c in self.clients:
                    c.sendall(f'update_btn_text,{",".join(self.multi_lobby_page.btn_clients[i].text if self.multi_lobby_page.btn_clients[i].text else "None" for i in range(5))}'.encode())
                break

    def run(self):
        print('Server started')
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

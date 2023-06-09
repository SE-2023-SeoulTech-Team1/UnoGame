import socket
import threading
import json

class Server:
    def __init__(self, multi_lobby_page):
        self.host = str(self.get_ip_address())
        self.port = 12345
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.multi_lobby_page = multi_lobby_page
        self.clients = []
        self.clients_name = []
        self.data = {'clients' : []}
        self.ready_clients = {}
        self.player_seleceted = [False for _ in range(5)]
        self.multi_lobby_page.btn_ip.text = self.host
        self.run()

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("10.255.255.255", 1))  # 아무 IP 주소
            IP = s.getsockname()[0]
        except:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def handle_client(self, client_socket, client_address):

        print(f'New client connected: {client_address}')
        name = client_socket.recv(1024).decode()
        print(f'{name} has connected.')

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                json_data = data.decode()
                message = json.loads(json_data)
                pwd = message.get("pwd")
                name = message.get("name")
                self.clients_name.append(name)
                if len(self.clients_name) > 5:
                    data = {'name' : name, 'enter_lobby' : False}
                    self.data['clients'].append(data)
                    self.multi_lobby_page.over_five = True

                    
                else:
                    if str(pwd) == "1234":
                        data = {'name' : name, 'enter_lobby' : True}
                        self.data['clients'].append(data)
                    else:
                        break

                # 응답 처리해서 클라이언트에게 다시 보내기 
                json_data = json.dumps(self.data)
                client_socket.sendall(json_data.encode())
                break
            except: 
                print("error!!")
                break
        while True:
            try:
                data = client_socket.recv(1024).decode()
                print(data)
                if not data:
                    break
                
                if data == "enter_lobby":
                    for i, c in enumerate(self.clients):
                        # player_selected도 같이 보내줌 
                        self.data['player_selected'] = self.multi_lobby_page.player_selected
                        json_data = json.dumps(self.data)
                        c.sendall(json_data.encode())
                    # 여기서 업데이트 
                    print(self.clients_name)
                    if len(self.clients_name) > 5:
                        print("5명을 초과하였습니다!")
                    
                    for i, player in enumerate(self.multi_lobby_page.player_selected):
                        if player and self.multi_lobby_page.btn_clients[i].text is "":
                            self.multi_lobby_page.btn_clients[i].text = self.clients_name[i]


            except:
                break

    def run(self):
        print('Server started')
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
          
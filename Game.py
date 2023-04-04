from Card import *
from random import shuffle
from Player import *

TIMEOUT = 10

class Game:
    def __init__(self, players):

        if not players:
            print("Number of Players should be at least one.")
            exit(-1)

        cards = [Card(color, type) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type) for type in BLACK_CARD_TYPES]
        shuffle(cards)

        self.deck = Deck(cards)
        self.players = players
        self.current_player_index = 0
        self.current_card = None
        self.direction = 1

    
    def auto_draw_card(self):
        print("카드 선택 시간을 초과하였습니다. 자동으로 카드를 뽑아옵니다.")
        self.players[self.current_player_index].draw_card(self.deck)
        return -1
    
    # 게임 시작 시 플레이어들에게 카드를 나눠주는 함수

    def deal_cards(self):
        for i in range(7):
            for player in self.players:
                player.cards.append(self.deck.pop_card())

    # 게임 시작 시 current card를 뽑는 함수

    def pick_current_card(self):
        while True:
            self.current_card = self.deck.pop_card()
            if self.current_card.color != "black":
                break
            else:
                self.deck.cards.append(self.current_card)
                shuffle(self.deck.cards)

    # 플레이어가 드로우 버튼을 클릭하는 함수

    def draw_card_clicked(self, player):
        player.draw_card(self.deck)
        
    
    # 플레이어의 턴을 진행하는 함수

    def next_turn(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        
    
    # 특수 카드 처리

    def reverse_card_clicked(self): 
        self.direction *= -1
       #self.current_player_index= None (index 값이 필요하면 정수형값 할당하시면 됩니다)
        self.next_turn()
        return self
    
    def skip_card_clicked(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        self.next_turn()
        return self
    
    def plus2_card_clicked(self, player):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        player = self.players[self.current_player_index]
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        self.next_turn()
        return self
    
    def wildcard_card_clicked(self, chosen_color):
        self.current_card.color = chosen_color
        print(self.current_card.color)
        self.next_turn()
        return self
    
    def plus4_card_clicked(self, player, chosen_color):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        player = self.players[self.current_player_index]
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        chosen_color = input(" ") 
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    #bombcard 추가(자신을 제외한 모든 플레이어가 카드를 3개씩 받음)
    
    def bombcard_card_clicked(self, player, chosen_color):
        player = self.players[self.current_player_index]
        for p in self.players:
            if p != player:
                for _ in range(3):
                    p.draw_card(self.deck)
        chosen_color = input(" ")
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
            
    #changecard 추가(자신의 카드를 2장 선택하여 덱에서 교환)
    
    def changecard_card_clicked(self, player, change_indices, chosen_color, card_index):
        player = self.players[self.current_player_index]
        change_indices = []
        #print("교환할 두 카드를 선택하세요.")
        for _ in range(2):
            card_index = int(input(" ")) -1
            change_indices.append(card_index)
            #print(f"{player.name} 님의 카드가 교환되었습니다.")
            #print(f"\n{player.name}의 카드는:")
        player.cards[change_indices[0]], player.cards[change_indices[1]] = self.deck.pop_card(), self.deck.pop_card()
        chosen_color = input("")
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    #copycard 추가 (선택한 다른 플레이어의 임의의 카드를 복사해 자신의 카드로 추가)
    
    def copy_card_clicked(self, player_index, chosen_color):
        player = self.players[self.current_player_index]
        target_player = self.players[player_index]
        target_player_cards = target_player.cards.copy()
        shuffle(target_player_cards)
        card = target_player_cards.pop()
        player.cards.append(card)
        """print(f"{player.name}님의 카드에 {card}가 추가되었습니다.")"""
        chosen_color = input(" ")
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    #changeall추가 (선택한 다른 플레이어의 모든 카드를 자신의 카드로 교환)
    
    def change_all_clicked(self, player_index, chosen_color):
        player = self.players[self.current_player_index]
        target_player = self.players[player_index]

        # 플레이어와 타겟 플레이어의 카드 리스트를 복사해둔다.
        player_cards = player.cards.copy()
        target_player_cards = target_player.cards.copy()

        # 카드를 교환한다.
        player.cards = target_player_cards
        target_player.cards = player_cards

        #print(f"{player.name}님의 모든 카드와 {target_player.name}님의 모든 카드가 교환되었습니다.")
        chosen_color = input(" ")
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    #게임 종료 조건
    def game_win(self, player):
        if len(player.cards) == 0:
            return True
        else:
            return False

          
"""""
    def start(self):
        # 카드 7장 나누기
        for i in range(7):
            for player in self.players:
                player.draw_card(self.deck)

        while True:
            self.current_card = self.deck.pop_card()
            if self.current_card.color != "black":
                break
            else:
                self.deck.cards.append(self.current_card)
                shuffle(self.deck.cards)

        while True:
            # 현재 플레이어
            player = self.players[self.current_player_index]

            # 현재 카드 출력
            print(f"\n현재 카드: {self.current_card}")

            # 플레이어의 카드 출력
            print(f"\n{player.name} 턴입니다. 당신의 카드는:")
            for i, card in enumerate(player.cards):
                print(f"{i+1}.{card}")

            # 카드를 선택하도록 요청
            card_index = int(input("카드를 선택하세요 (카드를 뽑으려면 0을 입력하세요): ")) -1

            # 플레이어가 카드를 뽑는 경우
            if card_index == -1:
                drawn_card = player.draw_card(self.deck)
                print(f"\n뽑은 카드: {drawn_card}")
                
                # 덱에 카드가 없는 경우
                if not self.deck.cards:
                    print("더이상 카드가 없습니다.")
                    break

            # 선택한 카드가 유효한 경우
            elif self.can_play(player.cards[card_index]):
                played_card = player.play_card(card_index)
                print(f"\n{player.name} 낸 카드는 {played_card}입니다")
                self.current_card = played_card
                
                # 특수 카드 처리
                
                if played_card.type == 'skip':
                    self.current_player_index = (self.current_player_index + self.direction ) % len(self.players) 
                elif played_card.type == 'reverse':
                    self.direction *= -1              
                elif played_card.type == '+2':
                    next_player_index = (self.current_player_index + self.direction) % len(self.players)
                    self.players[next_player_index].draw_card(self.deck)
                    self.players[next_player_index].draw_card(self.deck)
                elif played_card.type == 'wildcard':
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    self.current_card.color = chosen_color
                elif played_card.type == '+4':
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    next_player_index = (self.current_player_index + self.direction) % len(self.players)
                    self.players[next_player_index].draw_card(self.deck)
                    self.players[next_player_index].draw_card(self.deck)
                    self.players[next_player_index].draw_card(self.deck)
                    self.players[next_player_index].draw_card(self.deck)
                    self.current_card.color = chosen_color
                    
                elif played_card.type == 'bombcard':
                    for p in self.players:
                        if p != player:
                            for _ in range(3):
                                p.draw_card(self.deck)
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    self.current_card.color = chosen_color
                
                elif played_card.type == "changecard":
                    change_indices = []
                    print("교환할 두 카드를 선택하세요.")
                    for _ in range(2):
                        card_index = int(input("카드를 선택하세요: ")) -1
                        change_indices.append(card_index)
                    player.cards[change_indices[0]], player.cards[change_indices[1]] = self.deck.pop_card(), self.deck.pop_card()
                    print(f"{player.name} 님의 카드가 교환되었습니다.")
                    print(f"\n{player.name}의 카드는:")
                    for i, card in enumerate(player.cards):
                        print(f"{i+1}.{card}")
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    self.current_card.color = chosen_color
                
                elif played_card.type == "changeallcard":
                    while True:
                        target_index = int(input("몇 번 플레이어와 교환하시겠습니까? (1~4): ")) - 1
                        if target_index != self.current_player_index and target_index >= 0 and target_index < len(self.players):
                            break
                        print("잘못된 입력입니다. 다시 입력해주세요.")
                    self.change_all(target_index)
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    self.current_card.color = chosen_colo
                    
                elif played_card.type == "copycard":
                    while True:
                        target_index = int(input("몇 번 플레이어의 카드를 복사하시겠습니까? (1~4): ")) - 1
                        if target_index != self.current_player_index and target_index >= 0 and target_index < len(self.players):
                            break
                        print("잘못된 입력입니다. 다시 입력해주세요.")
                    self.copy_card(target_index)                    
                    chosen_color = input("Choose color (red, yellow, green, blue): ")
                    self.current_card.color = chosen_color
                    
                
                
                
                # 게임 종료
                if len(player.cards) == 0:
                    print(f"\n{player.name} 승리했습니다!")
                    break
                
            # 선택한 카드가 유효하지 않은 경우
            else:
                print("낼 수 없는 카드입니다.")
                continue
            self.current_player_index = (self.current_player_index + self.direction) % len(self.players)"""

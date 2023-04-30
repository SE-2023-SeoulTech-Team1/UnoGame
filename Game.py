from Card import *
from random import shuffle
from Player import *
import os

TIMEOUT = 10

class Game:
    def __init__(self, players, color_weak_mode=False):

        if not players:
            print("Number of Players should be at least one.")
            exit(-1)

        cards = [Card(color, type, color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, color_weak_mode) for type in BLACK_CARD_TYPES]
        if os.path.exists('game_state.pkl'):
            pass
        else: 
            shuffle(cards)

        self.deck = Deck(cards)
        self.players = players
        self.current_player_index = 0
        self.current_card = None
        self.direction = 1
        self.uno = None
        self.color_weak_mode = color_weak_mode
    
    def reset_deck(self, color_weak_mode=False):
        cards = [Card(color, type, color_weak_mode) for type in COLOR_CARD_TYPES for color in COLORS]
        cards += [Card("black", type, color_weak_mode) for type in BLACK_CARD_TYPES]
        shuffle(cards)
        
        self.deck = Deck(cards)
        

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
            if (self.current_card.color != "black" and
                self.current_card.type not in ['+2', 'skip', 'reverse']):
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
        # self.current_player_index = (self.current_player_index + self.direction) % len(self.players)
        tmp = (self.current_player_index + self.direction) % len(self.players)
        player = self.players[tmp]
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        self.next_turn()
        return self
    
    def wildcard_card_clicked(self, chosen_color):
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    def plus4_card_clicked(self, player, chosen_color):
        tmp = (self.current_player_index + self.direction) % len(self.players)
        player = self.players[tmp]
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        player.draw_card(self.deck)
        self.current_card.color = chosen_color
        self.next_turn()
        return self
    
    #bombcard 추가(자신을 제외한 모든 플레이어가 카드를 3개씩 받음)
    
    def bombcard_card_clicked(self, chosen_color):
        player = self.players[self.current_player_index]
        for p in self.players:
            if p != player:
                for _ in range(3):
                    p.draw_card(self.deck)
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
        self.current_card.color = chosen_color
        self.next_turn()
        return self

    def uno_button_clicked(self, player_idx):

        player_with_one_card = [player for player in self.players if len(player.cards) == 1]
        if not player_with_one_card:
            self.players[player_idx].draw_card(self.deck)
            return False

        if len(self.players[player_idx].cards) == 1:
            self.uno = player_idx
        else:
            for player in player_with_one_card:
                player.draw_card(self.deck)
        return True
    
    #게임 종료 조건
    def game_win(self, player):
        if len(player.cards) == 0:
            return True
        else:
            return False

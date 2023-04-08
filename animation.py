import pygame
pygame.init()

# 게임 창 크기 및 이름 설정
screenWidth = 800
screenHeight = 600
windowSize = (screenWidth, screenHeight)
screen = pygame.display.set_mode(windowSize)
pygame.display.set_caption("UNO GAME")

# 색상 정의
DARKGREEN = (8, 44, 15)
GREY = (25, 25, 25)
WHITE = (255, 255, 255)
RED = (185, 52, 31)
BLUE = (0, 0, 255)
GREEN = (0, 143, 0)
YELLOW = (255, 218, 71)
BLACK = (0, 0, 0)

SELECT_COLOR = {"red": RED, "green": GREEN, "blue": BLUE, "yellow": YELLOW}

# 폰트 설정
font = pygame.font.SysFont(None, 30)
unoFont = pygame.font.SysFont(None, 40)

# 기본 배경 설정
backgroundColor = DARKGREEN
playerBgColor = GREY
boardx = 0
boardy = 0
boardWidth = screenWidth*0.75
boardHeight = screenHeight
playerBgx = screenWidth*0.75
playerBgy = 0
playerBgWidth = screenWidth*0.25
playerBgHeight = screenHeight
directionBgx = screenWidth*0.2
directionBgy = 0
directionBgWidth = 100
directionBgHeight = 100

# 카드 이미지 불러오기
def cardFrontImg(color, type):
    return pygame.image.load('./assets/cards/' + color + type + '.png').convert_alpha()


# 카드 앞면 출력
def draw_card_front(screen, card, top, left):
    card_front_img = pygame.image.load(card.front).convert_alpha()
    screen.blit(card_front_img, (left, top))


# 카드 뒷면 출력
def draw_card_back(screen, card, top, left):
    card_back_img = pygame.image.load(card.back).convert_alpha()
    screen.blit(card_back_img, (left, top))

def drawGameScreen(screen, game):
    # 배경 색 설정/추후 배경사진 추가
    screen.fill(backgroundColor)

    # 플레이어 스크린 우측에 배치
    player_bg_rect = pygame.Rect(playerBgx, playerBgy, playerBgWidth, screenHeight)
    pygame.draw.rect(screen, playerBgColor, player_bg_rect)

    who_are_players = font.render("PLAYER", True, WHITE)
    players_rect = who_are_players.get_rect()
    players_rect.centerx = round(playerBgx + playerBgWidth*0.5)
    players_rect.y = 20
    screen.blit(who_are_players, players_rect)

    # 현재 방향 아이콘 표시
    if game.direction == 1:
        direction_icon = pygame.image.load("./assets/clockwise.png")
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))

    else:
        direction_icon = pygame.image.load("./assets/counterclockwise.png")
        direction_icon = pygame.transform.scale(direction_icon, (30, 30))
    screen.blit(direction_icon, (screen.get_width() * 0.06, screen.get_height() * 0.025))



def move_card_animation(screen, game, card, start_pos, end_pos, duration=500):
    start_time = pygame.time.get_ticks()
    elapsed_time = 0
    distance = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    card_img = pygame.image.load(card.front).convert_alpha()
    card_rect = card_img.get_rect()

    while elapsed_time < duration:
        elapsed_time = pygame.time.get_ticks() - start_time
        progress = min(elapsed_time / duration, 1)
        new_pos = start_pos[0] + distance[0] * progress, start_pos[1] + distance[1] * progress
        card_rect.x, card_rect.y = new_pos
        screen.blit(card_img, (card_rect.left, card_rect.top))
        pygame.display.flip()
        drawGameScreen(screen, game)

    # card_rect.x, card_rect.y = end_pos


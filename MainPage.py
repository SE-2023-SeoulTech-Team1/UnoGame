import pygame
from SettingPage import draw_settings_screen

# 게임 윈도우 초기화
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Uno Game")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont(None, 48)

# 메인 화면 그리기
def draw_main_screen():

    # 전역 변수 생성 
    global start_text, setting_text, quit_text

    screen.fill(WHITE)
    title_text = font.render("UNO GAME", True, BLACK)
    screen.blit(title_text, (screen_width//2 - title_text.get_width()//2, 70))
    start_text = font.render("START GAME", True, WHITE, GREEN)
    pygame.draw.rect(screen, GREEN, (screen_width//2 - start_text.get_width()//2 - 10, 220, start_text.get_width()+20, start_text.get_height()+20))
    screen.blit(start_text, (screen_width//2 - start_text.get_width()//2, 230))
    setting_text = font.render("SETTING", True, WHITE, BLUE)
    pygame.draw.rect(screen, BLUE, (screen_width//2 - setting_text.get_width()//2 - 10, 310, setting_text.get_width()+20, setting_text.get_height()+20))
    screen.blit(setting_text, (screen_width//2 - setting_text.get_width()//2, 320))
    quit_text = font.render("QUIT GAME", True, WHITE, RED)
    pygame.draw.rect(screen, RED, (screen_width//2 - quit_text.get_width()//2 - 10, 410, quit_text.get_width()+20, quit_text.get_height()+20))
    screen.blit(quit_text, (screen_width//2 - quit_text.get_width()//2, 420))

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            start_rect = pygame.Rect(screen_width//2 - start_text.get_width()//2 - 10, 210, start_text.get_width()+20, start_text.get_height()+20)
            if start_rect.collidepoint(mouse_x, mouse_y):
                print("Start game!")
            setting_rect = pygame.Rect(screen_width//2 - setting_text.get_width()//2 - 10, 300, setting_text.get_width()+20, setting_text.get_height()+20)
            if setting_rect.collidepoint(mouse_x, mouse_y):
                print("Setting!!")
                draw_settings_screen()
            quit_rect = pygame.Rect(screen_width//2 - quit_text.get_width()//2 - 10, 400, quit_text.get_width()+20, quit_text.get_height()+20)
            if quit_rect.collidepoint(mouse_x, mouse_y):
                running = False
    
    draw_main_screen()
    pygame.display.update()

pygame.quit()

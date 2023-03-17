import pygame
import pygame_gui

# 게임 윈도우 초기화
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Uno Game")

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FFFFFF'))



#ui매니저
ui_manager = pygame_gui.UIManager((screen_width, screen_height))


# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.SysFont(None, 48)

clock = pygame.time.Clock()

def draw_settings_screen():
    global running, clock
    screen.fill(WHITE)
    
    # 타이틀 텍스트 
    title_text = font.render("SETTINGS", True, BLACK)
    background.blit(title_text, (screen_width//2 - title_text.get_width()//2, 70))

    #창 크기 옵션 버튼 
    menu_rect = pygame.Rect(screen_width//2 - 75, 150, 150, 50)
    menu_options = ["800x600", "1024x768", "1280x1024"]
    menu = pygame_gui.elements.UIDropDownMenu(  
        options_list=menu_options,
        starting_option="800x600",
        relative_rect=menu_rect,
        manager= ui_manager
        )
    
    #키 설정 옵션 버튼
    key_rect = pygame.Rect(screen_width//2 - 75, 230, 150, 50)
    key_button = pygame_gui.elements.UIButton(
        relative_rect= key_rect,
        manager = ui_manager,
        text = "KEY SETTINGS")

    #색약 모드 버튼 

    color_rect = pygame.Rect(screen_width//2 - 75, 310, 150, 50)
    color_button = pygame_gui.elements.UIButton(
        relative_rect=color_rect,
        manager = ui_manager,
        text = "COLOR CHANGE"
    )



    # 뒤로가기 버튼 
    back_text = font.render("BACK", True, WHITE, BLUE)
    pygame.draw.rect(background, BLUE, (screen_width//2 - back_text.get_width()//2 - 10, 450, back_text.get_width()+20, back_text.get_height()+20))
    background.blit(back_text, (screen_width//2 - back_text.get_width()//2, 460))






    while True:
        #이게 뭐지 
        time_delta = clock.tick(120)/1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                back_rect = pygame.Rect(screen_width//2 - back_text.get_width()//2 - 10, 440, back_text.get_width() + 20, back_text.get_height() + 20)
                if back_rect.collidepoint(mouse_x, mouse_y):
                    return
                
                if key_rect.collidepoint(mouse_x, mouse_y):
                    print("세팅 버튼")

                if color_rect.collidepoint(mouse_x, mouse_y):
                    print("색약 버튼")
                
            elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == menu:
                    selected_option =event.text
                    print("Selected option: ", selected_option)
            ui_manager.process_events(event)

        ui_manager.update(time_delta)

        screen.blit(background, (0, 0))

        ui_manager.draw_ui(screen)

        pygame.display.update()



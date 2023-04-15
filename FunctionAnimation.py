import pygame as pg
import sys

def display_reverse_animation(screen, icon, duration=0.6):
    start_time = pg.time.get_ticks()
    elapsed_time = 0

    while elapsed_time < duration * 1000:
        # screen.fill((255, 255, 255))
        elapsed_time = pg.time.get_ticks() - start_time
        # opacity = int(255 * (1 - (elapsed_time / (duration * 1000))))

        icon_copy = icon.copy()
        # icon_copy.set_alpha(opacity)
        screen.blit(icon_copy, (screen.get_width() // 2 - icon.get_width() // 2, screen.get_height() // 2 - icon.get_height() // 2))

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

def display_skip_animation(screen, next_player, duration=0.6):
    start_time = pg.time.get_ticks()
    elapsed_time = 0
    font = pg.font.SysFont(None, 120)

    # 텍스트 
    next_player = font.render(next_player, True, pg.Color("white"))
    next_player_rect = next_player.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

    # 라인 

    line_pos = (next_player_rect.left, next_player_rect.centery)
    line_size = (next_player_rect.width, 10)

    while elapsed_time < duration * 1000:
        elapsed_time = pg.time.get_ticks() - start_time


        screen.blit(next_player, next_player_rect)

        pg.draw.line(screen, pg.Color("red"), line_pos, (line_pos[0]+line_size[0], line_pos[1]), line_size[1])


        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()


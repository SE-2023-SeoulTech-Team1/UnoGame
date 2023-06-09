import pygame

fps = 60
fpsClock = pygame.time.Clock()

pygame.init()
FONT = pygame.font.SysFont(None, 32)
WINNERFONT = pygame.font.SysFont('arialroundedmtblod', 100, True, True)

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (32, 32, 32)

RED = (255, 0, 0)
W_RED = (199, 109, 156)
RED_HOVER = "#820600"
RED_PRESSED = "#570400"

GREEN = (0, 255, 0)
W_GREEN = (0, 147, 102)

BLUE = (0, 0, 255)
W_BLUE = (80, 168, 233)

YELLOW = (255, 218, 71)
W_YELLOW = (226, 148, 8)
GRAY = (128, 128, 128)
LIGHT_GRAY = "#EEEEEE"

PINK = "#FFABAB"
NEON_GREEN = "#16FF00"
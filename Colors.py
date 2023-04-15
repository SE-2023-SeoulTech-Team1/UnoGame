import pygame

fps = 60
fpsClock = pygame.time.Clock()

pygame.init()
font = pygame.font.SysFont('arialroundedmtbold', 32)

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
RED_HOVER = "#820600"
RED_PRESSED = "#570400"
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = "#EEEEEE"
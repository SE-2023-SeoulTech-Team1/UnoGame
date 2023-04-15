import pygame
import sys

pygame.init()
font = pygame.font.SysFont('arial', 48)

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Button():
    def __init__(self, x,  y, width, height, text = 'Button'):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = screen_width * x
        self.left = screen_height * y
        # self.onclickFunction = onclickFunction
        # self.alreadyPressed = False
        # self.parameters = parameters

        self.fillColors = {
            'normal': '#A5140C',
            'hover': '#820600',
            'pressed': '#570400',
            'drop_normal': '#'
        }
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.top, self.left, self.width, self.height)
        self.text = font.render(text, True, BLACK)


    def process(self, screen, hover=False):

        screen_width, screen_height = pygame.display.get_surface().get_size()
        self.top = screen_width * self.x
        self.left = screen_height * self.y
        self.rect = pygame.Rect(self.top, self.left, self.width, self.height)

        self.hover = hover
        mousePos = pygame.mouse.get_pos()
        self.surface.fill(self.fillColors['normal'])

        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.fillColors['hover'])

        #     if pygame.mouse.get_pressed()[0]: # 왼쪽 마우스 버튼이 눌렸으면
        #         self.surface.fill(self.fillColors['pressed'])
            #     if not self.alreadyPressed:
            #         self.onclickFunction(*self.parameters)
            #         self.alreadyPressed = True
            # else:
            #     self.alreadyPressed = False

        self.surface.blit(self.text, [
            self.rect.width/2 - self.text.get_rect().width/2,
            self.rect.height/2 - self.text.get_rect().height/2
        ])

        # screen에 Surface 위치 시킴
        screen.blit(self.surface, self.rect)

        if hover == True:
            self.surfaceR.fill(self.fillColors['hover'])

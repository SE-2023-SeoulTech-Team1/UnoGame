import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pygame
from Button import Button

pygame.init()
screen = pygame.display.set_mode((600, 800))

def test_button_init():
    btn = Button(0.5, 0.5, 200, 50, text='Test Button', background_color=(255, 255, 255),
                 hover_color=(128, 128, 128), text_color=(0, 0, 0), text_size=24)
    assert btn.x == 0.5
    assert btn.y == 0.5
    assert btn.width == 200
    assert btn.height == 50
    assert btn.text == 'Test Button'
    assert btn.background_color == (255, 255, 255)
    assert btn.colors['hover'] == (128, 128, 128)
    assert btn.text_color == (0, 0, 0)
    assert btn.text_size == 24


def test_button_process():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    btn = Button(0.5, 0.5, 200, 50, text='Test Button', background_color=(255, 255, 255),
                 hover_color=(128, 128, 128), text_color=(0, 0, 0), text_size=24)

    # Test normal state
    btn.process(screen)
    assert btn.surface.get_at((0, 0)) == (255, 255, 255, 255)

    # Test hover state
    pygame.mouse.set_pos(320, 240)
    btn.process(screen, hover=True)
    assert btn.surface.get_at((0, 0)) == (128, 128, 128, 255)

    pygame.quit()


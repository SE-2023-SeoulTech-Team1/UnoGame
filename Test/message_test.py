import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pygame
import pytest
from unittest import mock
from Message import Message
from Colors import *


@pytest.fixture(scope="module")
def screen():
    pygame.init()
    return pygame.display.set_mode((640, 480))

@mock.patch('time.sleep', return_value=None)
def test_message_sleep(mock_sleep, screen):
    message = Message(screen, "Hello, world!", 32, (255, 255, 255))
    message.draw()
    assert mock_sleep.call_count == 1

import pygame
import settings
from typing import Tuple


class Missile(pygame.sprite.Sprite):
    '''
    Missile object represents a falling deadly missile

    Args:
        screen_pos (Tuple[int, int]): tuple of initial screen coordinates (pixels)

    Attributes:
        speed (int): missile's vertical speed
    '''

    def __init__(self, screen_pos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface(settings.missile_dimensions)
        self.image.fill(settings.missile_color)
        self.rect = self.image.get_rect(topleft=screen_pos)

        # missile's movement
        self.speed = settings.missile_speed

    def update(self, y_shift: int) -> None:
        '''
        Updates missile's position

        Args:
            y_shift (int): shift of missile's y coordinate
        '''
        self.rect.y += y_shift + self.speed

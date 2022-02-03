import pygame
import settings
from typing import Tuple


class Player(pygame.sprite.Sprite):
    '''
    Player object represents the player of the game

    Args:
        map_pos (Tuple[int, int]): tuple of initial map coordinates (tile numbers)

    Attributes:
        speed (int): player's horizontal speed
        jump_speed (int): player's jump "speed"
        gravity (float): player's gravity rate
        direction (pygame.math.Vector2(0, 0)): vector of player's horizontal and vertical direction
    '''
    def __init__(self, map_pos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface(settings.player_dimensions)
        self.image.fill(settings.player_and_text_color)
        screen_pos = (map_pos[0] * settings.tile_size,
                      map_pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(bottomleft=screen_pos)

        # player's movement
        self.speed = settings.horizontal_speed
        self.jump_speed = settings.jump_speed
        self.gravity = settings.gravity
        self.direction = pygame.math.Vector2(0, 0)

    def get_input(self) -> None:
        '''
        Gets keyboard input and sets player's movement
        '''
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.direction.y == 0:
            self.jump()

    def apply_gravity(self) -> None:
        '''
        Applies gravity to player
        '''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self) -> None:
        '''
        Makes player jump
        '''
        self.direction.y = self.jump_speed

    def update(self, y_shift: int) -> None:
        '''
        Updates player's position

        Args:
            y_shift (int): shift of player's y coordinate
        '''
        self.rect.y += y_shift
        self.get_input()

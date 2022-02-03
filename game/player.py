import pygame
import settings
from typing import Tuple

class Player(pygame.sprite.Sprite):
    def __init__(self, map_pos: Tuple[int, int]) -> None:
        super().__init__()
        self.image = pygame.Surface(settings.player_dimensions)
        self.image.fill(settings.player_and_text_color)
        screen_pos = (map_pos[0] * settings.tile_size,
                      map_pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(bottomleft=screen_pos)

        # player movement
        self.speed = settings.horizontal_speed
        self.jump_speed = settings.jump_speed
        self.gravity = settings.gravity
        self.direction = pygame.math.Vector2(0, 0)

    def get_input(self) -> None:
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
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self) -> None:
        self.direction.y = self.jump_speed

    def update(self, y_shift: int) -> None:
        self.rect.y += y_shift
        self.get_input()
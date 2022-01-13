import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, map_pos):
        super().__init__()
        self.image = pygame.Surface((30, 60))
        self.image.fill(settings.player_color)
        screen_pos = (map_pos[0] * settings.tile_size,
                      map_pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(bottomleft=screen_pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = settings.horizontal_speed
        self.gravity = settings.gravity
        self.jump_speed = settings.jump_speed

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.direction.y == 0:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self, y_shift):
        self.rect.y += y_shift
        self.get_input()

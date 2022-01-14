import pygame
import settings

class Missile(pygame.sprite.Sprite):
    def __init__(self, screen_pos):
        super().__init__()
        self.image = pygame.Surface(settings.missile_dimensions)
        self.image.fill(settings.missile_color)
        self.rect = self.image.get_rect(topleft=screen_pos)

        # missile movement
        self.speed = settings.missile_speed
        self.direction = pygame.math.Vector2(0, 0)

    def update(self, y_shift):
        self.rect.y += y_shift + self.speed
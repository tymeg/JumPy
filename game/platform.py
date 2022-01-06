import pygame
import settings


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, length):
        super().__init__()
        self.image = pygame.Surface((length*settings.tile_size, settings.tile_size))
        self.image.fill('grey')
        pos = (pos[0] * settings.tile_size, pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, y_shift):
        self.rect.y -= y_shift

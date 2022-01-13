import pygame
import settings


class Platform(pygame.sprite.Sprite):

    def __init__(self, map_pos, length, type, number):
        super().__init__()
        self.image = pygame.Surface(
            (length * settings.tile_size, settings.platform_thickness))

        # can be modified later
        self.type = type
        if type == 'normal':
            self.image.fill('white')
        elif type == 'bounce':
            self.image.fill('blue')
        elif type == 'collapse':
            self.image.fill('azure4')

        self.number = number
        self.map_coords = pygame.math.Vector2(map_pos[0], map_pos[1])

        screen_pos = (map_pos[0] * settings.tile_size,
                      map_pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(topleft=screen_pos)

    def update(self, y_shift):
        self.rect.y -= y_shift
        if self.rect.y > self.map_coords.y*settings.tile_size + settings.tile_size:
            self.map_coords.y += 1

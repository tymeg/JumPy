import pygame
import settings


class Platform(pygame.sprite.Sprite):

    def __init__(self, map_pos, length, type, number):
        super().__init__()
        self.image = pygame.Surface(
            (length * settings.tile_size, settings.platform_thickness))

        self.number = number
        self.type = type
        self.map_coords = pygame.math.Vector2(map_pos[0], map_pos[1])

        screen_pos = (map_pos[0] * settings.tile_size,
                      map_pos[1] * settings.tile_size)
        self.rect = self.image.get_rect(topleft=screen_pos)

        # can be modified later
        self.type = type
        if type == 'normal':
            self.image.fill(settings.normal_platform_color)
        elif type == 'bounce':
            self.image.fill(settings.bounce_platform_color)
        elif type == 'collapse':
            self.image.fill(settings.collapse_platform_color)
        elif type == 'horizontal':
            self.image.fill(settings.horizontal_platform_color)
            self.right = True
        elif type == 'vertical':
            self.image.fill(settings.vertical_platform_color)
            self.up = True
            self.level = 0

    def update(self, y_shift):
        self.rect.y += y_shift
        if self.rect.y > self.map_coords.y*settings.tile_size + settings.tile_size:
            self.map_coords.y += 1
        
        if self.type == 'horizontal':
            if self.right:
                self.rect.x += settings.horizontal_platform_speed
                if self.rect.right >= settings.screen_width:
                    self.right = False
            else: # left
                self.rect.x -= settings.horizontal_platform_speed
                if self.rect.left <= 0:
                    self.right = True

        if self.type == 'vertical':
            if self.up:
                self.level -= settings.vertical_platform_speed
                self.rect.y -= settings.vertical_platform_speed
                if self.level <= -settings.vertical_platform_range:
                    self.up = False
            else: # down
                self.level += settings.vertical_platform_speed
                self.rect.y += settings.vertical_platform_speed
                if self.level >= settings.vertical_platform_range:
                    self.up = True

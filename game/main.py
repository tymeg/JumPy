import pygame
import sys

import settings
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))
pygame.display.set_caption(settings.title)
clock = pygame.time.Clock()
font = pygame.font.SysFont(settings.font_name, settings.font_size, True)
level = Level(screen, font)

# Main game loop
while True:
    level.run()

    pygame.display.update()
    clock.tick(settings.fps)

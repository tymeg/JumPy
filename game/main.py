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
level = Level(screen)

# Main game loop
while True:
    level.run()

    pygame.display.update()
    clock.tick(settings.fps)

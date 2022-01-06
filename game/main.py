import pygame
import sys

import settings
from level import Level

# Pygame setup
pygame.init()
screen = pygame.display.set_mode(
    (settings.screen_width, settings.screen_height))
pygame.display.set_caption("Gierka")
clock = pygame.time.Clock()
level = Level(screen)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)

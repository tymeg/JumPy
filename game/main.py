'''
Module with game setup and main game loop
'''

import pygame

import settings
from game import Game

if __name__ == '__main__':
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode(
        (settings.screen_width, settings.screen_height))
    pygame.display.set_caption(settings.title)
    clock = pygame.time.Clock()

    logo = pygame.transform.scale(pygame.image.load(
        settings.logo_path).convert_alpha(), (settings.logo_width, settings.logo_height))
    pygame.display.set_icon(logo)

    big_font = pygame.font.SysFont(
        settings.font_name, settings.big_font_size, True)
    small_font = pygame.font.SysFont(
        settings.font_name, settings.small_font_size, True)
    fonts = {'big_font': big_font, 'small_font': small_font}

    game = Game(screen, logo, fonts)

    # Main game loop
    while True:
        game.run()

        pygame.display.update()
        clock.tick(settings.fps)

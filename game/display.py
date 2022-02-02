import pygame
import sys

import settings
from platforms import Platform
from player import Player
from missile import Missile

class Display:

    def __init__(self, surface, fonts):
        self.surface = surface
        self.fonts = fonts

    def score(self, score):
        score_text = self.fonts['big_font'].render(
            f"SCORE: {score}", True, settings.player_and_text_color)
        text_pos = (settings.screen_width/2 - score_text.get_width() // 2, 20)
        self.surface.blit(score_text, text_pos)

    def game(self, platforms, player, missiles, score):
        platforms.draw(self.surface)
        player.draw(self.surface)
        missiles.draw(self.surface)
        self.score(score)

    def game_over(self):
        text1 = self.fonts['big_font'].render(
            "GAME OVER!", True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            "PRESS ENTER TO RESTART", True, settings.player_and_text_color)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, settings.screen_height/2 - text1.get_height())
        text2_pos = (settings.screen_width/2 - text2.get_width() //
                     2, settings.screen_height/2 + 20)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)

    
#import pygame
#import sys

import settings


class Display:

    def __init__(self, surface, fonts):
        self.surface = surface
        self.fonts = fonts

    def game(self, platforms, player, missiles, score):
        self.surface.fill(settings.background_color)
        platforms.draw(self.surface)
        player.draw(self.surface)
        missiles.draw(self.surface)
        self.score(score)

    def score(self, score):
        score_text = self.fonts['big_font'].render(
            f"SCORE: {score}", True, settings.player_and_text_color)
        text_pos = (settings.screen_width/2 - score_text.get_width() // 2, 20)
        self.surface.blit(score_text, text_pos)

    def menu(self):
        self.surface.fill(settings.background_color)
        text1 = self.fonts['big_font'].render(
            settings.title, True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            "PRESS ENTER TO PLAY!", True, settings.player_and_text_color)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, settings.screen_height/2 - text1.get_height())
        text2_pos = (settings.screen_width/2 - text2.get_width() //
                     2, settings.screen_height/2 + 20)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)

    def pause(self):
        text1 = self.fonts['small_font'].render(
            "PAUSE", True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            "PRESS ESC TO RESUME", True, settings.player_and_text_color)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, 80)
        text2_pos = (settings.screen_width/2 - text2.get_width() //
                     2, 105)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)

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

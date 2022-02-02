import pygame
import sys

import settings
import scoreboard


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
            "PRESS ENTER TO CONTINUE", True, settings.player_and_text_color)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, settings.screen_height/2 - text1.get_height())
        text2_pos = (settings.screen_width/2 - text2.get_width() //
                     2, settings.screen_height/2 + 20)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)

    def input(self, nick):
        self.surface.fill(settings.background_color)
        text1 = self.fonts['small_font'].render(
            "ENTER YOUR NAME:", True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            nick, True, settings.player_and_text_color)

        self.surface.blit(text1, (50, 50))
        self.surface.blit(text2, (50, 75))

    def scoreboard(self):
        self.surface.fill(settings.background_color)
        text = self.fonts['big_font'].render(
            "SCOREBOARD", True, settings.player_and_text_color)
        self.surface.blit(text, (settings.screen_width /
                          2 - text.get_width() // 2, 50))
        scores = scoreboard.get_scoreboard()

        for count, row in enumerate(scores):
            left = self.fonts['small_font'].render(str(
                count + 1) + ". " + row.nick, True, settings.player_and_text_color)
            right = self.fonts['small_font'].render(
                str(row.score), True, settings.player_and_text_color)
            self.surface.blit(left, (50, 130 + count*30))
            self.surface.blit(right, (settings.screen_width -
                              50 - right.get_width(), 130 + count*30))

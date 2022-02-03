import pygame
from typing import Dict

import settings
import scoreboard


class Display:
    '''
    Display object has fields and methods to draw objects to the screen and display different game states

    Args:
        surface (pygame.Surface): game screen
        logo (pygame.Surface): game logo
        fonts (Dict[str, pygame.font.Font]): dictionary of fonts

    Attributes:
        surface (pygame.Surface): game screen
        logo (pygame.Surface): game logo
        fonts (Dict[str, pygame.font.Font]): dictionary of fonts
    '''

    def __init__(self, surface: pygame.Surface, logo: pygame.Surface, fonts: Dict[str, pygame.font.Font]) -> None:
        self.surface = surface
        self.logo = logo
        self.fonts = fonts

    def game(self, platforms: pygame.sprite.Group, player: pygame.sprite.GroupSingle, missiles: pygame.sprite.Group, score: int) -> None:
        '''
        Draws game objects

        Args:
            platforms (pygame.sprite.Group): group of current platforms in the game
            player (pygame.sprite.GroupSingle): single group containing the player
            missiles (pygame.sprite.Group): group of current missiles in the game
            score (int): current score
        '''
        self.surface.fill(settings.background_color)
        platforms.draw(self.surface)
        player.draw(self.surface)
        missiles.draw(self.surface)
        self.score(score)

    def score(self, score: int) -> None:
        '''
        Draws score

        Args:
            score (int): score to draw
        '''
        score_text = self.fonts['big_font'].render(
            f"SCORE: {score}", True, settings.player_and_text_color)
        text_pos = (settings.screen_width/2 - score_text.get_width() // 2, 20)
        self.surface.blit(score_text, text_pos)

    def menu(self) -> None:
        '''
        Draws menu state
        '''
        self.surface.fill(settings.background_color)

        text1 = self.fonts['big_font'].render(
            settings.title, True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            "by Tymeg", True, settings.player_and_text_color)
        text3 = self.fonts['small_font'].render(
            "PRESS ENTER TO PLAY!", True, settings.player_and_text_color)

        logo_pos = (70, 100)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, settings.screen_height - 250)
        text2_pos = (settings.screen_width - text2.get_width() -
                     135, settings.screen_height - 185)
        text3_pos = (settings.screen_width/2 - text3.get_width() //
                     2, settings.screen_height - 135)

        self.surface.blit(self.logo, logo_pos)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)
        self.surface.blit(text3, text3_pos)

    def pause(self) -> None:
        '''
        Draws pause state
        '''
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

    def game_over(self) -> None:
        '''
        Draws game over state
        '''
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

    def input(self, nick: str) -> None:
        '''
        Draws nick input state

        Args:
            nick (str): current nick characters 
        '''
        self.surface.fill(settings.background_color)
        text1 = self.fonts['small_font'].render(
            "ENTER YOUR NAME:", True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            nick, True, settings.player_and_text_color)

        self.surface.blit(text1, (50, 50))
        self.surface.blit(text2, (50, 80))

    def scoreboard(self) -> None:
        '''
        Draws scoreboard
        '''
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

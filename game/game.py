import pygame
import sys

from platforms import Platform
import settings
from player import Player
from missile import Missile
from random import randint, choice


class Game:
    def __init__(self, surface, fonts):

        # Custom events setup
        self.PLATFORM_COLLAPSE = pygame.USEREVENT + 1
        self.SPAWN_MISSILE = pygame.USEREVENT + 2

        # game setup
        self.display_surface = surface
        self.fonts = fonts
        self.new_game()

    def new_game(self):
        # reset
        pygame.event.clear()
        self.game_active = True
        self.score = 0
        self.collapsing = False
        self.collapsing_platforms = []
        self.world_shift = 0
        self.world_descend_speed = 0
        self.spawn_missiles = False
        self.spawn_collapse_platforms = False
        self.missile_spawn_frequency_down = settings.start_missile_spawn_frequency_down
        self.missile_spawn_frequency_up = settings.start_missile_spawn_frequency_up

        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.missiles = pygame.sprite.Group()

        # platforms
        start_platform = Platform(
            (0, settings.map_heigth-1), settings.map_width, 'normal', 0)
        self.platforms.add(start_platform)
        top_level, top_number = start_platform.map_coords.y, 0
        for i in range(9):
            new_platform = self.generate_new_platform(top_level, top_number)
            top_level, top_number = new_platform.map_coords.y, new_platform.number
            self.platforms.add(new_platform)

        # player
        player_sprite = Player(settings.start_pos)
        self.player.add(player_sprite)

    def missile_queue(self):
        pygame.time.set_timer(self.SPAWN_MISSILE, randint(self.missile_spawn_frequency_down, self.missile_spawn_frequency_up), 1)

    def spawn_missile(self):
        missile = Missile((randint(0, settings.screen_width - settings.missile_dimensions[0]), -100))
        self.missiles.add(missile)

    def generate_new_platform(self, top_level, top_number):
        if not self.spawn_collapse_platforms:
            return Platform((randint(0, 7), top_level - randint(2, 4)), randint(2, 3), choice(settings.platform_types[:-1]), top_number + 1)
        else:
            return Platform((randint(0, 7), top_level - randint(2, 4)), randint(2, 3), choice(settings.platform_types), top_number + 1)

    def manage_platforms_and_missiles(self):
        bottom_platform = self.platforms.sprites()[0]

        if bottom_platform.rect.y > settings.screen_height:
            self.platforms.remove(bottom_platform)

            top_platform = self.platforms.sprites()[len(
                self.platforms.sprites()) - 1]
            new_platform = self.generate_new_platform(
                top_platform.map_coords.y, top_platform.number)
            self.platforms.add(new_platform)
        
        if self.missiles.sprites():
            bottom_missile = self.missiles.sprites()[0]
            if bottom_missile.rect.y > settings.screen_height:
                self.missiles.remove(bottom_missile)

    def scroll_y(self):
        player = self.player.sprite

        if player.rect.y < settings.scroll_border and player.direction.y < 0:
            self.world_shift = settings.scroll_speed
            player.rect.y += settings.scroll_speed
            for missile in self.missiles.sprites():
                missile.rect.y += settings.scroll_speed

            # world starts descending, missiles spawn, collapse platforms spawn only after first scroll
            if self.world_descend_speed == 0:
                self.world_descend_speed = settings.start_world_descend_speed       
                self.missile_queue()
                self.spawn_missiles = True
                self.spawn_collapse_platforms = True
        else:
            self.world_shift = 0

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # for platform in self.platforms.sprites():
        #     if platform.rect.colliderect(player.rect):
        #         if player.direction.x < 0:
        #             player.rect.left = platform.rect.right
        #         elif player.direction.x > 0:
        #             player.rect.right = platform.rect.left

    def platform_type_action(self, platform):
        player = self.player.sprite

        if platform.type == 'bounce':
            player.jump_speed = settings.bounce_speed
            player.jump()
            player.jump_speed = settings.jump_speed
        elif platform.type == 'collapse' and not self.collapsing:
            pygame.time.set_timer(self.PLATFORM_COLLAPSE, 500, 1)
            self.collapsing_platforms.append(platform)
            self.collapsing = True

    def vertical_movement_collision(self):
        self.player.sprite.apply_gravity()
        player = self.player.sprite

        for platform in self.platforms.sprites():
            if platform.rect.colliderect(player.rect):
                if player.direction.y > 0 and player.rect.bottom - player.direction.y <= platform.rect.top:
                    player.rect.bottom = platform.rect.top
                    player.direction.y = 0
                    if self.score < platform.number:
                        self.score = platform.number
                    self.platform_type_action(platform)
                # elif player.direction.y < 0:
                #     player.rect.top = platform.rect.bottom
                #     player.direction.y = 1

    def platform_collapse(self):
        self.platforms.remove(self.collapsing_platforms[0])
        self.collapsing_platforms.pop(0)

        top_platform = self.platforms.sprites(
        )[len(self.platforms.sprites()) - 1]
        new_platform = self.generate_new_platform(
            top_platform.map_coords.y, top_platform.number)
        self.platforms.add(new_platform)
        self.collapsing = False

    def adjust_game_difficulty(self):
        if self.score >= 25 and self.score < 50:
            self.world_descend_speed = 2
            self.missile_spawn_frequency_down = 4000 
            self.missile_spawn_frequency_up = 8000
        elif self.score >= 50 and self.score < 100:
            self.world_descend_speed = 3
            self.missile_spawn_frequency_down = 3000 
            self.missile_spawn_frequency_up = 6000
        elif self.score >= 100 and self.score < 150:
            self.world_descend_speed = 5
            self.missile_spawn_frequency_down = 2000 
            self.missile_spawn_frequency_up = 4000
        elif self.score >= 150:
            self.world_descend_speed = 7
            self.missile_spawn_frequency_down = 1000 
            self.missile_spawn_frequency_up = 2000

    def display_score(self):
        score_text = self.fonts['big_font'].render(
            f"SCORE: {self.score}", True, settings.player_and_text_color)
        text_pos = (settings.screen_width/2 - score_text.get_width() // 2, 20)
        self.display_surface.blit(score_text, text_pos)

    def game_over(self):
        player = self.player.sprite

        hit_by_missile = False
        for missile in self.missiles.sprites():
            if missile.rect.colliderect(player.rect):
                hit_by_missile = True
                break

        if player.rect.right < 0 or player.rect.left > settings.screen_width or player.rect.bottom >= settings.screen_height or hit_by_missile:
            player.rect.x, player.rect.y = settings.start_pos[0], settings.start_pos[1]
            return True
        return False

    def show_game_over_screen(self):
        text1 = self.fonts['big_font'].render("GAME OVER!", True, settings.player_and_text_color)
        text2 = self.fonts['small_font'].render(
            "PRESS ENTER TO RESTART", True, settings.player_and_text_color)
        text1_pos = (settings.screen_width/2 - text1.get_width() //
                     2, settings.screen_height/2 - text1.get_height())
        text2_pos = (settings.screen_width/2 - text2.get_width() //
                     2, settings.screen_height/2 + 20)
        self.display_surface.blit(text1, text1_pos)
        self.display_surface.blit(text2, text2_pos)

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_active:
                if event.type == self.PLATFORM_COLLAPSE:
                    self.platform_collapse()
                elif event.type == self.SPAWN_MISSILE:
                    if self.spawn_collapse_platforms:
                        self.spawn_missile()
                        self.missile_queue()
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.new_game()

        if self.game_active:
            self.display_surface.fill(settings.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # platforms
            self.scroll_y()
            self.manage_platforms_and_missiles()
            self.platforms.update(self.world_shift + self.world_descend_speed)
            self.platforms.draw(self.display_surface)

            # player
            self.player.update(self.world_descend_speed)
            self.horizontal_movement_collision()
            self.vertical_movement_collision()
            self.player.draw(self.display_surface)

            # missiles
            self.missiles.update(self.world_descend_speed)
            self.missiles.draw(self.display_surface)

            # score
            self.display_score()
            self.adjust_game_difficulty()

            # game over
            if self.game_over():
                self.game_active = False
                self.show_game_over_screen()

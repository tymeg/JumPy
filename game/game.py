import pygame
import sys

import settings
from display import Display
from platforms import Platform
from player import Player
from missile import Missile
from random import randint, choice


class Game:
    def __init__(self, surface, fonts):

        # Custom events setup
        self.PLATFORM_COLLAPSE = pygame.USEREVENT + 1
        self.SPAWN_MISSILE = pygame.USEREVENT + 2

        # game setup
        self.display = Display(surface, fonts)
        self.new_game()

    def new_game(self):
        # reset
        pygame.event.clear()
        self.game_active = True
        self.score = 0
        self.collapsing = False
        self.collapsing_platforms = []
        self.world_shift = 0
        self.spawn_missiles = False
        self.spawn_collapse_platforms = False

        self.set_game_difficulty(settings.game_difficulty[0])
        self.world_descend_speed = 0

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
        pygame.time.set_timer(self.SPAWN_MISSILE, randint(
            self.missile_spawn_frequency_down, self.missile_spawn_frequency_up), 1)

    def spawn_missile(self):
        missile = Missile(
            (randint(0, settings.screen_width - settings.missile_dimensions[0]), -100))
        self.missiles.add(missile)

    def generate_new_platform(self, top_level, top_number):
        if not self.spawn_collapse_platforms:
            platform = Platform((randint(0, 7), top_level - randint(2, 4)), randint(
                2, 3), choice(settings.platform_types[:-1]), top_number + 1)
            return platform
        else:
            platform = Platform((randint(0, 7), top_level - randint(2, 4)),
                                randint(2, 3), choice(settings.platform_types), top_number + 1)
            return platform

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
                self.world_descend_speed = settings.game_difficulty[0]['world_descend_speed']
                self.missile_queue()
                self.spawn_missiles = True
                self.spawn_collapse_platforms = True
        else:
            self.world_shift = 0

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
        elif platform.type == 'horizontal':
            if platform.right:
                player.rect.x += (settings.horizontal_platform_speed)
            else:
                player.rect.x -= (settings.horizontal_platform_speed)
        elif platform.type == 'vertical':
            if platform.up:
                player.rect.y -= (settings.vertical_platform_speed)
            else:
                player.rect.y += (settings.vertical_platform_speed)

    def vertical_movement_collision(self):
        self.player.sprite.apply_gravity()
        player = self.player.sprite

        for platform in self.platforms.sprites():
            stands = (platform.rect.top == player.rect.bottom and player.rect.right >=
                      platform.rect.left and player.rect.left <= platform.rect.right)
            if platform.rect.colliderect(player.rect) or stands:
                if player.direction.y > 0 and player.rect.bottom - player.direction.y - 1 <= platform.rect.top:
                    player.rect.bottom = platform.rect.top
                    player.direction.y = 0
                    if self.score < platform.number:
                        self.score = platform.number
                    self.platform_type_action(platform)

    def horizontal_movement(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

    def platform_collapse(self):
        self.platforms.remove(self.collapsing_platforms[0])
        self.collapsing_platforms.pop(0)

        top_platform = self.platforms.sprites(
        )[len(self.platforms.sprites()) - 1]
        new_platform = self.generate_new_platform(
            top_platform.map_coords.y, top_platform.number)
        self.platforms.add(new_platform)
        self.collapsing = False

    def set_game_difficulty(self, parameters):
        self.world_descend_speed = parameters['world_descend_speed']
        self.missile_spawn_frequency_down = parameters['missile_spawn_frequency_down']
        self.missile_spawn_frequency_up = parameters['missile_spawn_frequency_up']

    def adjust_game_difficulty(self):
        if self.score >= settings.score_thresholds[0] and self.score < settings.score_thresholds[1]:
            self.set_game_difficulty(settings.game_difficulty[1])
        elif self.score >= settings.score_thresholds[1] and self.score < settings.score_thresholds[2]:
            self.set_game_difficulty(settings.game_difficulty[2])
        elif self.score >= settings.score_thresholds[2] and self.score < settings.score_thresholds[3]:
            self.set_game_difficulty(settings.game_difficulty[3])
        elif self.score >= settings.score_thresholds[3]:
            self.set_game_difficulty(settings.game_difficulty[4])

    def game_over(self):
        player = self.player.sprite

        hit_by_missile = False
        for missile in self.missiles.sprites():
            if missile.rect.colliderect(player.rect):
                hit_by_missile = True
                break

        game_over_position = (player.rect.right < 0 or player.rect.left >
                              settings.screen_width or player.rect.bottom >= settings.screen_height or hit_by_missile)
        if game_over_position:
            player.rect.x, player.rect.y = settings.start_pos[0], settings.start_pos[1]
            return True
        return False

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
                    if event.key == pygame.K_RETURN:  # ENTER
                        self.new_game()

        if self.game_active:
            self.display.surface.fill(settings.background_color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # ====== STATE ======
            # player
            self.horizontal_movement()
            self.vertical_movement_collision()
            self.player.update(self.world_descend_speed)

            # platforms and missiles
            self.manage_platforms_and_missiles()
            self.platforms.update(self.world_shift + self.world_descend_speed)
            self.missiles.update(self.world_descend_speed)

            # scroll screen
            self.scroll_y()

            # adjust game difficulty based on current score
            self.adjust_game_difficulty()

            # ====== DISPLAY ======
            self.display.game(self.platforms, self.player, self.missiles, self.score)

            # game over
            if self.game_over():
                self.game_active = False
                self.display.game_over()

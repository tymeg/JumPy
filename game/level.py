import pygame
import sys

from platforms import Platform
import settings
from player import Player
from random import randint, choice


class Level:
    def __init__(self, surface):

        # Custom events setup
        self.MANAGE_PLATFORMS = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MANAGE_PLATFORMS, 1000)

        self.PLATFORM_COLLAPSE = pygame.USEREVENT + 2

        # game setup
        self.display_surface = surface
        self.new_game()

    def new_game(self):
        self.collapsing = False
        self.world_shift = 0
        self.world_descend_speed = 0
        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # platforms
        start_platform = Platform(
            (0, settings.map_heigth-1), settings.map_width, 'normal')
        self.platforms.add(start_platform)
        toplevel = start_platform.map_coords.y
        for i in range(9):
            new_platform = self.generate_new_platform(toplevel)
            toplevel = new_platform.map_coords.y
            self.platforms.add(new_platform)

        # player
        player_sprite = Player(settings.start_pos)
        self.player.add(player_sprite)

    def generate_new_platform(self, toplevel):
        return Platform((randint(0, 8), toplevel - randint(2, 4)), randint(2, 3), choice(settings.platform_types))

    def manage_platforms(self):
        # world starts descending after first scroll
        if self.world_descend_speed == 0 and self.platforms.sprites()[0].rect.y > settings.screen_height:
            self.world_descend_speed = settings.start_world_descend_speed

        removed = 0
        while self.platforms.sprites()[0].rect.y > settings.screen_height:
            self.platforms.remove(self.platforms.sprites()[0])
            removed += 1

        toplevel = self.platforms.sprites()[len(self.platforms.sprites()) - 1].map_coords.y
        for i in range(removed):
            new_platform = self.generate_new_platform(toplevel)
            toplevel = new_platform.map_coords.y
            self.platforms.add(new_platform)

    def scroll_y(self):
        player = self.player.sprite

        if player.rect.y < (settings.screen_height/3) and player.direction.y < 0:
            self.world_shift = -settings.scroll_speed
            player.rect.y += settings.scroll_speed
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
            self.platform_collapse = platform
            self.collapsing = True

    def vertical_movement_collision(self):
        self.player.sprite.apply_gravity()
        player = self.player.sprite

        for platform in self.platforms.sprites():
            if platform.rect.colliderect(player.rect):
                if player.direction.y > 0 and player.rect.bottom - player.direction.y <= platform.rect.top:
                    player.rect.bottom = platform.rect.top
                    player.direction.y = 0
                    self.platform_type_action(platform)
                # elif player.direction.y < 0:
                #     player.rect.top = platform.rect.bottom
                #     player.direction.y = 1

    def game_over(self):
        player = self.player.sprite
        if player.rect.right < 0 or player.rect.left > settings.screen_width or player.rect.bottom >= settings.screen_height:
            self.new_game()

    def run(self):
        self.display_surface.fill(settings.background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == self.MANAGE_PLATFORMS:
                self.manage_platforms()
            elif event.type == self.PLATFORM_COLLAPSE:
                self.platforms.remove(self.platform_collapse)
                new_platform = self.generate_new_platform(
                    self.platforms.sprites()[len(self.platforms.sprites()) - 1].map_coords.y)
                self.platforms.add(new_platform)
                self.collapsing = False

        self.game_over()

        # platforms
        self.scroll_y()
        self.platforms.update(self.world_shift - self.world_descend_speed)
        self.platforms.draw(self.display_surface)

        # player
        self.player.update(self.world_descend_speed)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

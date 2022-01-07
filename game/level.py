import pygame
from platforms import Platform
import settings
from player import Player
from random import randint

class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.new_game()

    def new_game(self):
        self.clock = 0
        self.world_shift = 0
        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.should_spawn = True

        # Platforms
        start_platform = Platform((0, settings.map_heigth-1), settings.map_width)
        self.platforms.add(start_platform)
        toplevel = start_platform.map_coords.y
        for i in range(9):
            new_platform = self.generate_new_platform(toplevel)
            toplevel = new_platform.map_coords.y
            self.platforms.add(new_platform)

        # Player
        player_sprite = Player(settings.start_pos)
        self.player.add(player_sprite)

    def generate_new_platform(self, toplevel):
        return Platform((randint(0, 8), toplevel-randint(2, 4)), randint(1, 3))

    def manage_platforms(self):
        while self.platforms.sprites()[0].rect.y > settings.screen_height:
            self.platforms.remove(self.platforms.sprites()[0])
            new_platform = self.generate_new_platform(self.platforms.sprites()[len(self.platforms.sprites()) - 1].map_coords.y)
            self.platforms.add(new_platform)

    def scroll_y(self):
        player = self.player.sprite

        if player.rect.y < (settings.screen_height/3) and player.direction.y < 0:
            self.world_shift = -settings.speed
            # player.gravity = 1.2
        else:
            self.world_shift = 0
            # player.gravity = settings.gravity
            # player.jump_speed = settings.jump_speed
            # player.speed = settings.speed

    # def scroll_x(self):
    #     player = self.player.sprite
    #     player_x = player.rect.centerx
    #     direction_x = player.direction.x

    #     if player_x < (settings.screen_width / 4) and direction_x < 0:
    #         self.world_shift = settings.speed
    #         player.speed = 0
    #     elif player_x > (3.0/4.0 * settings.screen_width) and direction_x > 0:
    #         self.world_shift = -settings.speed
    #         player.speed = 0
    #     else:
    #         self.world_shift = 0
    #         player.speed = settings.speed

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        # for sprite in self.platforms.sprites():
        #     if sprite.rect.colliderect(player.rect):
        #         if player.direction.x < 0:
        #             player.rect.left = sprite.rect.right
        #         elif player.direction.x > 0:
        #             player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for platform in self.platforms.sprites():
            if platform.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = platform.rect.top
                    player.direction.y = 0
                # elif player.direction.y < 0:
                #     player.rect.top = sprite.rect.bottom
                #     player.direction.y = 1

    def game_over(self):
        player = self.player.sprite
        if player.rect.right < 0 or player.rect.left > settings.screen_width or player.rect.bottom > settings.screen_height:
            self.new_game()

    def run(self):
        self.game_over()

        if self.clock == settings.fps:
            self.manage_platforms()
            self.clock = 0
        else: self.clock += 1

        # platforms
        self.scroll_y()
        self.platforms.update(self.world_shift)
        self.platforms.draw(self.display_surface)


        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

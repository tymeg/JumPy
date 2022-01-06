import pygame
from platform import Platform
import settings
from player import Player
from random import randint

class Level:
    def __init__(self, surface):

        # level setup
        self.display_surface = surface
        self.new_game()

    def new_game(self):
        self.world_shift = 0
        self.current_x = 0
        self.platforms = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.should_spawn = True

        # Platforms - to generalize!
        start_platform = Platform((0, settings.map_heigth-1), settings.map_width)
        platform1 = Platform((1, 11), 2)
        platform2 = Platform((3, 8), 2)
        platform3 = Platform((6, 5), 2)
        platform4 = Platform((0, 2), 2)
        self.platforms.add(start_platform)
        self.platforms.add(platform1)
        self.platforms.add(platform2)
        self.platforms.add(platform3)
        self.platforms.add(platform4)

        # Player
        player_sprite = Player(settings.start_pos)
        self.player.add(player_sprite)

    def scroll_y(self):
        player = self.player.sprite
        player_y = player.rect.y
        direction_y = player.direction.y

        if player_y < (settings.screen_height / 2) and direction_y < 0:
            self.world_shift = -settings.speed
            player.speed = 0

            if self.should_spawn:
                platforms = self.platforms.sprites()
                self.platforms.remove(platforms[0])
                
                new_platform = Platform((randint(0, 9), randint(0, 2)), 2)
                self.platforms.add(new_platform)
                self.should_spawn = False
        else:
            self.world_shift = 0
            player.speed = settings.speed

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

        for sprite in self.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.platforms.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    self.should_spawn = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1

    def game_over(self):
        player = self.player.sprite
        if player.rect.x < 0 or player.rect.x > settings.screen_width or player.rect.y > settings.screen_height:
            self.new_game()

    def run(self):
        player = self.player.sprite
        
        # brzydkie? tu czy nie tu?
        self.game_over()

        # platforms
        self.platforms.update(self.world_shift)
        self.scroll_y()
        self.platforms.draw(self.display_surface)


        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.player.draw(self.display_surface)

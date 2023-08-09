import pygame

from settings import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]

        #graphic
        full_path = f'assets/weapon/{player.weapon}/{direction}.png'
        self.image = pygame.transform.scale(pygame.image.load(full_path), (16 * GAME_UPSCALE, 16 * GAME_UPSCALE)).convert_alpha()

        #place weapon
        if direction == 'right' :
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-GAME_UPSCALE, 0))
        elif direction == 'left' :
           self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(GAME_UPSCALE, 0))
        elif direction == 'up' :
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(0, GAME_UPSCALE))
        elif direction == 'down' :
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(0, 0))
import pygame
from settings import *

class Tile(pygame.sprite.Sprite) : 
    def __init__(self, position, groups, sprite_type, surface = pygame.Surface((TILE_SIZE * GAME_UPSCALE, TILE_SIZE * GAME_UPSCALE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect  = self.image.get_rect(topleft= position)
        self.hitbox = self.rect.inflate(GAME_UPSCALE*5, GAME_UPSCALE*10) #inflate pour respecter bord d'eau peut etre pas adapter au autre tile


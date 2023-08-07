import pygame

from settings import *
from src.entity import Entity, SpriteSheet


class House(Entity):

    def __init__(self, position, groups):
        super().__init__(groups)
        
        spritesheet_image = pygame.image.load(house_data['graphic']['asset']).convert_alpha()
        spritesheet_sprite = SpriteSheet(spritesheet_image)
        self.image = spritesheet_sprite.get_image(0, 0, 80, 80)
        position[0] -= TILE_SIZE*GAME_UPSCALE*2
        position[1] -= TILE_SIZE*GAME_UPSCALE*2
        self.rect = self.image.get_rect(topleft = position)

        self.hitbox = self.rect.inflate(0, 0).move(0, 0)

        #stats
        self.health = house_data['health']
        
    def interact(self):
        print("J'ai toucher la maison")



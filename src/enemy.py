import pygame
from settings import *
from src.entity import Entity

class Enemy(Entity):
    def __init__(self, monster_name, position, groups):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphic
        self.image = pygame.Surface((64, 64))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft= position)
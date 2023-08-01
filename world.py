import pygame
from settings import *
from tile import Tile

class World():
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # spirte group setup
        self.ground_sprites = pygame.sprite.Group()
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
    def run(self, player):
        #update and draw the game
        self.ground_sprites.draw(self.display_surface)
        self.visible_sprites.draw(player)
        self.visible_sprites.update()
        
    def createWorld(self):
        for col in range(int(HEIGHT/TILE_SIZE)):
            for row in range(int(WIDTH/TILE_SIZE)):
                x = row * TILE_SIZE
                y= col * TILE_SIZE
                Tile((x,y), [self.ground_sprites])   
        
class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]/2
        self.half_height = self.display_surface.get_size()[1]/2
        self.offset = pygame.math.Vector2()

    def draw(self, player):
        
        #getting the offset
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        self.offset.x = 0
        self.offset.y = 0
        
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.y):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
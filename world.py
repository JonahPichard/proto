import pygame

class World():
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # spirte group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        
    def run(self, player):
        #update and draw the game
        self.visible_sprites.draw(player)
        self.visible_sprites.update()
        
        
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
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y =0
        
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.y):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
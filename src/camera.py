import pygame


class CameraPosition():
    def __init__(self, rect : pygame.Rect):
        self.display_surface = pygame.display.get_surface()
        self.screen_offset = pygame.Vector2(self.display_surface.get_size())/2
        
        self.rect = rect
        self.offset = pygame.math.Vector2()
        self.ground_offset = pygame.math.Vector2()

    def position_update(self, player ):
        self.offset = player.rect.center - self.screen_offset
        self.ground_offset = self.rect.topleft - self.offset


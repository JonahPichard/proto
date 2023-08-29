import pygame

from settings import *
from src.camera import CameraPosition

from debug import debug

class LightGroups(pygame.sprite.Group):
    def __init__(self, camera: CameraPosition):
        super().__init__()
        self.camera = camera

    def add_light(self, filter):
        for light in self.sprites():
            position = self.camera.offset
            light.draw(filter,position)


class SimpleLight(pygame.sprite.Sprite) :
    def __init__(self, groups, rect : pygame.Rect, position, radius):
        super().__init__(groups)
        self.entity_rect = rect
        self.relative_position = position
        self.radius = radius

        self.asset = pygame.Surface([self.radius*2, self.radius*2], pygame.SRCALPHA, 32)
        self.asset.fill((255,255,255,255))
        pygame.draw.circle(self.asset, (255,255,255,0),[self.radius, self.radius],radius)

    def draw(self, surface : pygame.Surface,position):
        absolute_position = self.entity_rect.topleft - self.relative_position - position - (self.radius,self.radius)
        surface.blit(self.asset, absolute_position, special_flags=pygame.BLEND_RGBA_MIN)


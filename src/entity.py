import pygame
from math import sin
from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        
        #movement
        self.direction = pygame.math.Vector2()
        
        #graphic setup
        self.frame_index = 0
        self.status = 'down_idle'
        self.animation_speed = 0.15
        
    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed * GAME_UPSCALE
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed * GAME_UPSCALE
        self.collision('vertical')
        
        self.rect.midbottom = self.hitbox.midbottom
        
    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index +=self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        # self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def interact(self):
        pass

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else :
            return 0
            
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image.convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width * GAME_UPSCALE, height * GAME_UPSCALE))
        image.set_colorkey('black')
        image.convert()

        return image
import pygame
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
        
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        self.collision('vertical')
        
        self.rect.center = self.hitbox.center
        
    def collision(self, direction):
        # TODO enemy collision
        # TODO Hitbox du player doit seulement etre  sur ces pied
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
        self.rect = self.image.get_rect(center = self.hitbox.center)

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
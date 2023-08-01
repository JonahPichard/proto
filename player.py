import pygame
from settings import *

class Player(pygame.sprite.Sprite) : 
    def __init__(self, position, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -5)
        
    def import_players_assets(self):
        pass
        
    def input(self):
        keys = pygame.key.get_pressed()
        #movement inputdsq
        if keys[pygame.K_z]:
            self.direction.y =-1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
            
        if keys[pygame.K_q]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
            
            
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        # self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        # self.collision('vertical')
        
        self.rect.center = self.hitbox.center
        
    # def collision(self, direction):
    #     if direction == 'horizontal':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.x > 0:
    #                     self.hitbox.right = sprite.hitbox.left
    #                 elif self.direction.x < 0:
    #                     self.hitbox.left = sprite.hitbox.right
    #     if direction == 'vertical':
    #         for sprite in self.obstacle_sprites:
    #             if sprite.hitbox.colliderect(self.hitbox):
    #                 if self.direction.y > 0:
    #                     self.hitbox.bottom = sprite.hitbox.top
    #                 elif self.direction.y < 0:
    #                     self.hitbox.top = sprite.hitbox.bottom
    

    def update(self):
        self.input()
        self.move()
        
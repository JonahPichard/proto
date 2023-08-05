import pygame
from PIL import Image
from settings import *

class Minimap(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.coef = 4
        self.surface = pygame.Surface((WIDTH/self.coef, HEIGHT/self.coef))
        self.surface.fill((0, 0, 0))
        self.rect = self.surface.get_rect()
        self.screen = screen
        self.raw_image = Image.open("assets\map\png\map_empty_80_45.png").resize((self.surface.get_width(), self.surface.get_height()), Image.ANTIALIAS)
        self.raw_image.putalpha(210)
        self.raw_image.save("assets\map\png\minimap.png")
        self.raw_image = pygame.image.load("assets\map\png\minimap.png")
        
        pygame.draw.rect(self.raw_image, ((85, 70, 33)), self.rect, 2)
        
 
    def update(self, player, spawned_enemy):
        self.image = self.raw_image.copy()
        
        # print(player.rect.center)
        player_x, player_y = player.rect.center
        pygame.draw.circle(self.image, ((0, 0, 255)), (player_x/self.coef**2, player_y/self.coef**2), 2)

        for enemy in spawned_enemy:
            enemy_x, enemy_y = enemy.rect.center
            if enemy.health > 0:
                pygame.draw.circle(self.image, ((255, 0, 0)), (enemy_x/self.coef**2, enemy_y/self.coef**2), 2) 
        
        self.screen.blit(self.image, (WIDTH - self.surface.get_width() - 10 , 10))

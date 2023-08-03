import pygame
from settings import *
from src.tile import Tile
from debug import debug

from src.player import Player
from src.weapon import Weapon
from src.enemy import Enemy

import random

class World():
    def __init__(self):
        
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # spirte group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        #attack sprites
        self.current_attack = None

        #sprite setup
        self.createWorld()
        
    def run(self):
        #update and draw the game
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)

    def createAttack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destory_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def createWorld(self):
        # for col in range(int(HEIGHT/TILE_SIZE)):
        #     for row in range(int(WIDTH/TILE_SIZE)):
        #         x = row * TILE_SIZE
        #         y= col * TILE_SIZE
        #         Tile((x,y), [self.ground_sprites])

        self.player = Player((WIDTH / 2, HEIGHT / 2), [self.visible_sprites],self.obstacle_sprites,  self.createAttack, self.destory_attack)
        self.spawnEnemy(5)

    def spawnEnemy(self, numberOfEnemy):
        enemy_list = []
        for enemy in monster_data.keys():
            enemy_list.append(enemy)

        gap = 100
        for _ in range(numberOfEnemy):
            positions = [[random.randint(0 + gap, 200), random.randint(800, WIDTH - gap)], [random.randint(0 + gap, 200), random.randint(500, HEIGHT - gap)]]
            position = [positions[0][random.randint(0, 1)], positions[1][random.randint(0, 1)]]
            Enemy((enemy_list[random.randint(0, len(enemy_list)-1)]), position, [self.visible_sprites], self.obstacle_sprites)
       
class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]/2
        self.half_height = self.display_surface.get_size()[1]/2
        self.offset = pygame.math.Vector2()
        
        self.ground_surf = pygame.image.load('assets\map_empty_80_45.png').convert()
        self.ground_rect = self.ground_surf.get_rect(topleft= (0, 0))

    def draw(self, player):
        
        #getting the offset
        # self.offset.x = player.rect.centerx - self.half_width
        # self.offset.y = player.rect.centery - self.half_height
        self.offset.x = 0
        self.offset.y = 0
        
        ground_surf_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_surf_pos)
        
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'] 
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
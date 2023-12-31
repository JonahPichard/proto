import random
from enum import Enum

import pygame
from settings import *
from src.tile import Tile
from debug import debug

from src.player import Player
from src.weapon import Weapon
from src.enemy import Enemy
from src.house import House
from src.toolbox.import_world import get_info_map, distance
from src.ui import UI
from src.particle import AnimationPlayer
from src.upgrade import Upgrade
from src.daycycle import DayCycle
from src.light import LightGroups
from src.camera import CameraPosition


class World():
    def __init__(self):
        
        self.game_paused = False
        # map
        self.map_name = EMPTY_MAP

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        #Background surface
        self.ground_surf = pygame.image.load('assets\\map\\png\\map_empty_80_45.png').convert()
        self.ground_surf = pygame.transform.scale(self.ground_surf, (WIDTH * GAME_UPSCALE, HEIGHT * GAME_UPSCALE))
        self.ground_rect = self.ground_surf.get_rect(topleft= (0, 0))
        
        # Camera
        self.camera = CameraPosition(self.ground_rect)

        # spirte group setup
        self.visible_sprites = YsortCameraGroup(self.camera)
        self.light_source_sprite = LightGroups(self.camera)
        self.obstacle_sprites = pygame.sprite.Group()
        self.interact_sprite = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # mob spawn zone 
        self.mob_spawn = []
        #attack sprites
        self.current_attack = None

        #matrix
        self.matrix = [[1 for _ in range(WIDTH // TILE_SIZE)] for _ in range(HEIGHT // TILE_SIZE)]

        #sprite setup
        self.createWorld()
        self.daycycle = DayCycle(self.light_source_sprite)

        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        #particle
        self.animation_player = AnimationPlayer()

    def run(self, dt):
        self.camera.position_update(self.player)
        self.visible_sprites.update(dt)
        self.visible_sprites.enemy_update(self.player)
        self.daycycle.update_state(dt)

        self.visible_sprites.draw(self.ground_surf, self.player)
        self.player_attack_logic()
        self.daycycle.draw()
        self.ui.display(self.player, self.spawned_enemy)
        if self.game_paused:
            self.upgrade.display()
        else:
            #update and draw the game
            self.visible_sprites.update(dt)
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()

    def createAttack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destory_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None
        
    def createWorld(self):
        player_spawn = []
        house_spawn = []
        layout = get_info_map(self.map_name)
        for style, layer in layout.items():
            for row_index, row in enumerate(layer):
                for col_index, tile_id in enumerate(row):
                    x = col_index * TILE_SIZE * GAME_UPSCALE
                    y = row_index * TILE_SIZE * GAME_UPSCALE
                    if tile_id != 0 :
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                            self.matrix[row_index][col_index] = 0
                        else:
                            self.matrix[row_index][col_index] = 1
                        if style =='entity':
                            #TODO : automatiser tile_id dans Tiled
                            if tile_id == 82 :
                                player_spawn.append([x, y])
                            if tile_id == 80 :
                                self.mob_spawn.append([x, y])
                            if tile_id == 81 :
                                house_spawn.append([x, y])
        # TODO faire une fonction pour chech if empty
        if len(player_spawn) == 0 :
            player_spawn.append([WIDTH/2, HEIGHT/2])
            # TODO ficher de log
            print(f'INFO - Pas de tile de spawn du joueur dans {self.map_name}')
        if len(self.mob_spawn) == 0 :
            self.mob_spawn.append([WIDTH/2, HEIGHT/2])
            print(f'INFO - Pas de tile de spawn des ennemies dans {self.map_name}')
        if len(house_spawn) == 0 :
            house_spawn.append([WIDTH/2, HEIGHT/2])
            print(f'INFO - Pas de tile de spawnde la maison dans {self.map_name}')
        
        self.player = Player((random.choice(player_spawn)), [self.visible_sprites], self.obstacle_sprites, self.createAttack, self.destory_attack, self.light_source_sprite)   
        self.house = House((random.choice(house_spawn)), [self.visible_sprites, self.obstacle_sprites, self.interact_sprite])
        self.spawnEnemy(0)

    def spawnEnemy(self, numberOfEnemy):
        enemy_list = []
        self.spawned_enemy = []
        gap = 100
        for enemy in monster_data.keys():
            enemy_list.append(enemy)
        for _ in range(numberOfEnemy):
            position = random.choice(self.mob_spawn)
            enemy = Enemy(  (enemy_list[random.randint(0, len(enemy_list)-1)]),
                            position,
                            self.matrix,
                            [self.visible_sprites, self.attackable_sprites],
                            self.obstacle_sprites,
                            self.damage_player,
                            self.trigger_death_particles)
            self.spawned_enemy.append(enemy)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                            position = target_sprite.rect.center
                            self.animation_player.create_particle(position, 'slash', [self.visible_sprites])

    def damage_player(self, damage_ammount, attack_type):
        if self.player.vulnerable:
            self.player.health -= damage_ammount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
    
    def trigger_death_particles(self, position, particle_type):
        self.animation_player.create_particle(position, 'smoke', [self.visible_sprites])

    def open_menu(self):
        self.game_paused = not self.game_paused

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self, camera: CameraPosition):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.camera = camera

    def draw(self, surface : pygame.surface, player : Player):
        self.display_surface.blit(surface, self.camera.ground_offset)
        for sprite in sorted(self.sprites() , key= lambda sprite : sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.camera.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player : Player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'] 
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

import pygame, random
from settings import *
from src.tile import Tile
from debug import debug

from src.player import Player
from src.weapon import Weapon
from src.enemy import Enemy
from src.toolbox.import_world import get_info_map
from src.ui import UI
from src.particle import AnimationPlayer
from src.upgrade import Upgrade

class World():
    def __init__(self):
        
        self.game_paused = False
        # map
        self.map_name = EMPTY_MAP
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # spirte group setup
        self.visible_sprites = YsortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # mob spawn zone 
        self.mob_spawn = []
        #attack sprites
        self.current_attack = None

        #sprite setup
        self.createWorld()

        #user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        
        #particle
        self.animation_player = AnimationPlayer()
        
    def run(self):
        self.visible_sprites.draw(self.player)
        self.ui.display(self.player, self.spawned_enemy)
        
        if self.game_paused:
            self.upgrade.display()
        else:
            #update and draw the game
            self.visible_sprites.update()
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
        layout = get_info_map(self.map_name)
        for style, layer in layout.items():
            for row_index, row in enumerate(layer):
                for col_index, tile_id in enumerate(row):
                    x = col_index * TILE_SIZE * GAME_UPSCALE
                    y = row_index * TILE_SIZE * GAME_UPSCALE
                    if tile_id != 0 :
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                        if style =='data':
                            if tile_id == 11 :
                                player_spawn.append([x, y])
                            if tile_id == 22 :
                                self.mob_spawn.append([x, y])
        
        if len(player_spawn) == 0 :
            player_spawn.append([WIDTH/2, HEIGHT/2])
            # TODO ficher de log
            print(f'INFO - Pas de tile de spawn du joueur dans {self.map_name}')
        if len(self.mob_spawn) == 0 :
            self.mob_spawn.append([WIDTH/2, HEIGHT/2])
            print(f'INFO - Pas de tile de spawn des ennemies dans {self.map_name}')
        
        self.player = Player((random.choice(player_spawn)), [self.visible_sprites], self.obstacle_sprites, self.createAttack, self.destory_attack)   
        self.spawnEnemy(10)

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
    def __init__(self):
        
        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]/2
        self.half_height = self.display_surface.get_size()[1]/2
        self.offset = pygame.math.Vector2()
        
        # TODO Agrandir la map avec de l'eau pour ne pas voir le noir sur les bord de la map       
        self.ground_surf = pygame.image.load('assets\\map\\png\\map_empty_80_45.png').convert()
        # TODO Remplacer WIDTH et HEIGHT par la vrai taiile de la map
        self.ground_surf = pygame.transform.scale(self.ground_surf, (WIDTH * GAME_UPSCALE, HEIGHT * GAME_UPSCALE))
        self.ground_rect = self.ground_surf.get_rect(topleft= (0, 0))

    def draw(self, player):
        
        #getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # self.offset.x = 0
        # self.offset.y = 0
        
        ground_surf_pos = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf, ground_surf_pos)
        
        for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy'] 
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
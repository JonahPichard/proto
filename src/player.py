import pygame
from settings import *
from enum import Enum
from src.entity import *
from src.light import SimpleLight

from debug import debug

class Player(Entity) : 
    def __init__(self, position, groups, obstacle_sprites, create_attack, destory_attack, light_group):
        super().__init__(groups)
        
        spritesheet_image = pygame.image.load('assets/player/idle.png').convert_alpha()
        spritesheet_sprite = SpriteSheet(spritesheet_image)
        self.image = spritesheet_sprite.get_image(0, 0, 16, 16)
        self.rect = self.image.get_rect(topleft = position)
        hb_y_size_reduc = 10
        self.hitbox = self.rect.inflate(0,-hb_y_size_reduc*GAME_UPSCALE).move(0,hb_y_size_reduc/2*GAME_UPSCALE)

        #stats
        self.stats = player_data
        self.health = self.stats['health']
        self.gold = 0

        #movement attributes
        self.speed = self.stats['speed']
        self.obstacle_sprites = obstacle_sprites

        #weapon
        self.create_attack = create_attack
        self.destory_attack = destory_attack
        self.weapon_index = 0
        self.weapon = list(weapons_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.swicth_weapon_cooldown = PLAYER_SWITCH_WEAPON_COOLDOWN

        #Attack attributes
        self.attack_time = None
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.attacking = False
        self.damage = self.stats['damage']
           
        #graphic setup
        self.import_player_assets()
        
        #controller
        self.joysticks = []
        self.deadzone = 0.4

        #get damage attributes
        self.vulnerable = True
        self.hit_time = None
        self.invicilibilty_duration = 500

        #Light
        relative_position = pygame.math.Vector2(self.rect.topleft) - self.rect.center
        SimpleLight(light_group, self.rect, relative_position, 200)
    
    def import_player_assets(self):
        character_path = 'assets/player'
        self.animations = { 'down_idle' : [], 'up_idle' : [], 'left_idle' : [], 'right_idle' : [],
                            'down_walk' : [], 'up_walk' : [], 'left_walk' : [], 'right_walk' : [],
                            'down_attack' : [], 'up_attack' : [], 'left_attack' : [], 'right_attack' : [],
                            'down_dead' : [], 'up_dead' : [], 'left_dead' : [], 'right_dead' : []}
        row = 0
        for spritesheet in self.animations.keys() :
            full_path = f"{character_path}/{spritesheet.split('_')[1]}.png"
            spritesheet_image = pygame.image.load(full_path).convert_alpha()
            spritesheet_sprite = SpriteSheet(spritesheet_image)

            num_rows = spritesheet_image.get_height() // TILE_SIZE
            for col in range(num_rows):
                self.animations[spritesheet].append(spritesheet_sprite.get_image(row%4 * 16, col * 16, 16, 16))
            row+=1

    def get_status(self):
        if self.attacking :
            #arrete le joueur s'il attaque
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'attack')
                elif 'walk' in self.status:
                    self.status = self.status.replace('walk', 'attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
        
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                if 'walk' in self.status:
                    self.status = self.status.replace('walk', 'idle')
                else:
                    self.status = self.status + '_idle'
        else:
            if not 'walk' in self.status :
                if 'idle' in self.status:
                    self.status = self.status.replace('idle', 'walk')
                elif 'attack' in self.status:
                    self.status = self.status.replace('attack', 'walk')
                else:
                    self.status = self.status + '_walk'
        
    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            mouses = pygame.mouse.get_pressed()
            #movement input
            if keys[pygame.K_z]:
                self.direction.y =-1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
                
            if keys[pygame.K_q]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
                
            #attack input
            if mouses[0]:
                self.attack()
            
            '''
            Joystick
            '''
            if len(self.joysticks) > 0:
                joystick = self.joysticks[0]
                
                #movement
                if joystick.get_axis(1) < -self.deadzone:
                    self.direction.y =-1
                    self.status = 'up'
                elif joystick.get_axis(1) > self.deadzone:
                    self.direction.y = 1
                    self.status = 'down'
                else:
                    self.direction.y = 0
                    
                if joystick.get_axis(0) < -self.deadzone:
                    self.direction.x = -1
                    self.status = 'left'
                elif joystick.get_axis(0) > self.deadzone:
                    self.direction.x = 1
                    self.status = 'right'
                else:
                    self.direction.x = 0
                
                #attack
                if joystick.get_button(0):
                    self.attack()
                # swicth_weapon
                elif joystick.get_button(3):
                    self.switch_weapon()
                    
    def switch_weapon(self):
        if self.can_switch_weapon :
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            self.weapon_index = (self.weapon_index + 1) % len(list(weapons_data))
            self.weapon = list(weapons_data.keys())[self.weapon_index]
    
    def get_full_weapon_damage(self):
        base_damage = self.damage
        weapon_damage = weapons_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapons_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destory_attack()
                
        if not self.can_switch_weapon : 
            if current_time - self.weapon_switch_time >= self.swicth_weapon_cooldown:
                self.can_switch_weapon = True

        if not self.vulnerable:
             if current_time - self.hit_time >= self.invicilibilty_duration:
                self.vulnerable = True
                
    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)

        x, y = self.rect.centerx // TILE_SIZE // GAME_UPSCALE, self.rect.centery // TILE_SIZE // GAME_UPSCALE

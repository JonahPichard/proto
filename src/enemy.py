import pygame, random
from settings import *
from src.entity import *

class Enemy(Entity):
    def __init__(self, monster_name, position, groups, obstacle_sprites, damage_player, trigger_death_particles):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphic
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft= position)
        self.hitbox = self.rect.inflate(0, -10)

        #movement
        self.obstacle_sprites = obstacle_sprites

        #stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.gold_amount = monster_info['gold_amount']
        self.speed = monster_info['speed']
        self.damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        #init movement
        self.change_direction_cooldown = 2000
        self.moving_time = pygame.time.get_ticks()
        self.direction.x = random.randint(-1, 1) 
        self.direction.y = random.randint(-1, 1)

        #player interaction
        self.state = 'idle'
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 500
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

        #invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invicilibilty_duration = 300

    def import_graphics(self, name):
        self.animations = { 'down_idle' : [], 'up_idle' : [], 'left_idle' : [], 'right_idle' : []}
        enemy_path = f'assets/monster/{name}'
        for animation in self.animations.keys():
            row = 0
            for spritesheet in self.animations.keys() :
                full_path = f"{enemy_path}/{spritesheet.split('_')[1]}.png"
                spritesheet_image = pygame.image.load(full_path).convert_alpha()
                spritesheet_sprite = SpriteSheet(spritesheet_image)

                num_rows = spritesheet_image.get_height() // TILE_SIZE
                for col in range(num_rows):
                    self.animations[spritesheet].append(spritesheet_sprite.get_image(row%4 * 16, col * 16, 16, 16))
                row+=1

    def get_player_distance_and_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0 :
            direction =  (player_vec - enemy_vec).normalize()
        else : 
            direction = pygame.math.Vector2()
        
        return distance, direction

    def get_status(self, player):
        distance =  self.get_player_distance_and_direction(player)[0]
        if distance <= self.attack_radius:
            self.state = 'attack'
            self.status = 'down_idle'
        elif distance <= self.notice_radius:
            self.state = 'move'
            self.status = 'down_idle'
        else :
            self.state = 'idle'
            self.status = 'down_idle'

        if not self.vulnerable:
            self.state = 'hit'
            # self.status = 'down_hit'

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
                self.hit_time = pygame.time.get_ticks()
                self.vulnerable = False

    def actions(self, player):
        if self.state == 'attack':
            self.can_attack = False
            self.damage_player(self.damage, self.attack_type)
            self.attack_time = pygame.time.get_ticks()
        elif self.state == 'move':
            self.direction = self.get_player_distance_and_direction(player)[1]
        elif self.state =='hit':
            self.direction = self.get_player_distance_and_direction(player)[1]
            self.direction *= - 1/self.resistance

    def check_death(self, player):
        if self.health <= 0:
            player.gold += self.gold_amount
            self.trigger_death_particles(self.rect.center, 'smoke')
            self.kill()

    def update(self):
        self.cooldowns()
        self.animate()
        self.move(self.speed)
        
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.check_death(player)
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.state == 'idle':
            if current_time - self.moving_time >= self.change_direction_cooldown:
                self.direction.x = random.randint(-1, 1) 
                self.direction.y = random.randint(-1, 1)
                self.moving_time = pygame.time.get_ticks()
        
        if self.state == 'attack' and self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invicilibilty_duration:
                self.vulnerable = True
                

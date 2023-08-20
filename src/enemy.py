import pygame, random
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from settings import *
from src.entity import *

from debug import *

class Enemy(Entity):
    def __init__(self, monster_name, position, matrix, groups, obstacle_sprites, damage_player):
        super().__init__(groups)
        self.sprite_type = 'enemy'
        
        #graphic
        self.import_graphics(monster_name)
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft= position)
        self.hitbox = self.rect.inflate(0, -10)

        #movement
        self.obstacle_sprites = obstacle_sprites
        
        #path
        self.matrix = matrix
        self.path = []
        self.collision_rects = []
        self.pathfinder = Pathfinder(self.matrix, self)

        self.calculate_path = True
        self.path_time = None
        self.path_cooldown = 1000

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
            # self.direction = self.get_player_distance_and_direction(player)[1]
            if self.calculate_path :
                self.pathfinder.create_path(player)
                self.path_time = pygame.time.get_ticks()
                self.calculate_path = False
        elif self.state =='hit':
            self.direction = self.get_player_distance_and_direction(player)[1]
            self.direction *= - 1/self.resistance

    def check_death(self, player):
        if self.health <= 0:
            player.gold += self.gold_amount
            self.kill()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.centerx += self.direction.x * speed * GAME_UPSCALE
        self.collision('horizontal')
        self.hitbox.centery += self.direction.y * speed * GAME_UPSCALE
        self.collision('vertical')
        self.check_collisions()
        self.rect.midbottom = self.hitbox.midbottom

        

    def update(self):
        self.cooldowns()
        self.animate()
        self.move(self.speed)
        self.pathfinder.update()
        
        
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

        if not self.calculate_path:
            if current_time - self.path_time >= self.path_cooldown:
                self.calculate_path = True


    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.rect.center)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            if (end - start).magnitude() != 0:
                self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []

    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for node in self.path:
                x = (node.x * TILE_SIZE * GAME_UPSCALE) + TILE_SIZE * GAME_UPSCALE/2
                y = (node.y * TILE_SIZE * GAME_UPSCALE) + TILE_SIZE * GAME_UPSCALE/2
                rect = pygame.Rect((x - TILE_SIZE/2,y - TILE_SIZE/2),(TILE_SIZE,TILE_SIZE))
                self.collision_rects.append(rect)
    
    def check_collisions(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.hitbox.center):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.pathfinder.empty_path()
                


class Pathfinder:
    def __init__(self,matrix, enemy):
    # setup
        self.matrix = matrix
        self.grid = Grid(matrix = matrix)

        # pathfinding
        self.path = []

        #enemy
        self.enemy = enemy
        
        #screen
        self.display_surface = pygame.display.get_surface()

    def empty_path(self):
        self.path = []

    def create_path(self, player):
        # start
        start_x, start_y = self.enemy.get_coord()
        start = self.grid.node(start_x,start_y)

        # end
        end_x,end_y =  player.get_coord()
        end = self.grid.node(end_x,end_y)

        # path
        # finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start,end,self.grid)
        self.grid.cleanup()
        self.enemy.set_path(self.path)

    def draw_path(self):
        if self.path:
            points = []
            for node in self.path:
                x = (node.x * TILE_SIZE * GAME_UPSCALE) + TILE_SIZE * GAME_UPSCALE/2
                y = (node.y * TILE_SIZE * GAME_UPSCALE) + TILE_SIZE * GAME_UPSCALE/2
                points.append((x,y))

            pygame.draw.lines(self.display_surface,'#4a4a4a',False,points,5)

    def update(self):
        pass
        # self.draw_path()
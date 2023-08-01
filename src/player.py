import pygame
from settings import *

class Player(pygame.sprite.Sprite) : 
    def __init__(self, position, groups):
        super().__init__(groups)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill('blue')
        self.rect = self.image.get_rect(topleft = position)
        self.hitbox = self.rect.inflate(0, -5)
        
        #movement attributes
        self.direction = pygame.math.Vector2()
        self.speed = PLAYER_SPEED
        
        #Attack attributes
        self.attack_time = None
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.attacking = False
        self.attack_point = PLAYER_ATTACK_POINTS
        
        #health attributes
        self.health_point = PLAYER_HEALTH_POINTS
        
        self.import_player_assets()
    
    def import_player_assets(self):
        character_path = 'assets/player'
        self.animations = { 'idle' : [], 'walk': [], 'attack' : [], 'dead' : []}
        
        for spritesheet in self.animations.keys() :
            full_path = f"{character_path}/{spritesheet}.png"
            spritesheet_image = pygame.image.load(full_path)
            spritesheet_sprite = SpriteSheet(spritesheet_image)
            frame = 0
            for row in range(0, spritesheet_image.get_width(), TILE_SIZE):
                for col in range(0, spritesheet_image.get_height(), TILE_SIZE):
                    self.animations[spritesheet][row][col] = spritesheet_sprite.get_image(frame, row, col, 3, black)
                    frame += 1
                
        
    def animate(self):
        for row in range(0, spritesheet_image.get_width(), TILE_SIZE):
                for col in range(0, spritesheet_image.get_height(), TILE_SIZE):
        
    def input(self):
        keys = pygame.key.get_pressed()
        mouses = pygame.mouse.get_pressed()
        
        #movement input
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
            
        #attack input
        if mouses[0] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            print('attack')    
            
    def move(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * self.speed
        # self.collision('horizontal')
        self.hitbox.y += self.direction.y * self.speed
        # self.collision('vertical')
        
        self.rect.center = self.hitbox.center
        
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

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
    
    def update(self):
        self.input()
        self.cooldowns()
        self.move()
        
        
class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image
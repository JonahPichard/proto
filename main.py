import pygame, sys
from settings import *
from debug import debug
from world import World
from player import Player


class Game:
    def __init__(self):
        
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Proto')
        self.clock = pygame.time.Clock()
        
        '''
        Init Element
        '''     
        self.world = World()
        self.world.createWorld()
        self.player = Player((10, 10), [self.world.visible_sprites])
        
    def run(self):
        while True:
            
            '''
            Display Elements
            '''
            self.screen.fill('black')
            self.world.run(self.player)
            
            
            '''
            Event Handler
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()
            self.clock.tick(FPS)
            
            

if __name__ == '__main__':
    game = Game()
    game.run()
import pygame, sys
from settings import *

class Game:
    def __init__(self):
        
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Proto')
        self.clock = pygame.time.Clock()      
        
    def run(self):
        while True:

            self.screen.fill('black')
            
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
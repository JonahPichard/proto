import sys, cProfile

import pygame

from settings import *
from debug import debug
from src.world import World


class Game:
    def __init__(self):
        
        #general setup
        pygame.init()
        pygame.joystick.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Proto')
        self.clock = pygame.time.Clock()
        
        '''
        Init Element
        '''     
        self.world = World()
           
    def run(self):
        while True:
            
            '''
            Display Elements
            '''
            self.screen.fill('black')
            self.world.run()
            
            '''
            Event Handler
            '''
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_m : 
                        self.world.spawnEnemy(5)
                    elif event.key == pygame.K_e :
                        self.world.entity_interact()
                elif event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.world.player.joysticks.append(joy)
                    print("Controller connected, keyboard don't work ")
                elif event.type == pygame.MOUSEWHEEL:
                    self.world.player.switch_weapon()
            debug(f"FPS : {int(self.clock.get_fps())}", x=self.screen.get_width() - 100)

            pygame.display.update()
            self.clock.tick(FPS)
            
            

if __name__ == '__main__':
    game = Game()
    # cProfile.run("game.run()")
    game.run()
    
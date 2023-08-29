import sys, time, argparse, cProfile

import pygame
from settings import *
from debug import debug
from src.world import World


class Game:
    def __init__(self, size= None):
        
        #general setup
        pygame.init()
        pygame.joystick.init()
        if size == None:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        elif size == 'full':
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('Proto')
        self.clock = pygame.time.Clock()
        
        # delta time
        self.dt = 0
        self.prevtime = time.time()
        '''
        Init Element
        '''     
        self.world = World()
           
    def run(self):
        while True:
            self.dt = time.time() - self.prevtime
            self.prevtime = time.time()
            '''
            Display Elements
            '''
            self.screen.fill('#1e7cb8')
            self.world.run(self.dt)
            
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
                    elif event.key == pygame.K_u:
                        self.world.open_menu()
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
    # parser = argparse.ArgumentParser(description='Description de votre programme')
    # parser.add_argument('settings', type=str, help='Description du paramètre')
    # args = parser.parse_args()
    
    # game = Game(args.settings)
    game = Game()
    # cProfile.run("game.run()")
    game.run()
    
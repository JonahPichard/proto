import sys, time, argparse, cProfile
from enum import Enum, auto

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

        # game world
        self.world = World()

        # Game State
        self.debug_collision = False
           
    def run(self):
        while True:
            self.dt = time.time() - self.prevtime
            self.prevtime = time.time()
            '''
            Display Elements
            '''
            self.screen.fill('#1e7cb8')
            self.world.run(self.dt)
            
            self.event_handler()

            # debug
            if self.debug_collision:
                self.debug_colision()

            debug(f"FPS : {int(self.clock.get_fps())}", x=self.screen.get_width() - 100)
            pygame.display.update()
            self.clock.tick(FPS)

    def event_handler(self):
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
                    elif event.key == pygame.K_p :
                        self.debug_collision = not self.debug_collision

                elif event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.world.player.joysticks.append(joy)
                    print("Controller connected, keyboard don't work ")
        
                elif event.type == pygame.MOUSEWHEEL:
                    self.world.player.switch_weapon()

    def debug_colision(self):
        color = (255,0,0)
        sprite : pygame.sprite.Sprite
        for sprite in self.world.obstacle_sprites :
            rect = sprite.hitbox
            rect_position = rect.topleft - self.world.camera.offset
            rect_value = (*rect_position, *rect.size)
            pygame.draw.rect(self.screen, color, rect_value, 5)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Description de votre programme')
    # parser.add_argument('settings', type=str, help='Description du paramètre')
    # args = parser.parse_args()
    
    # game = Game(args.settings)
    game = Game()
    # cProfile.run("game.run()")
    game.run()
    
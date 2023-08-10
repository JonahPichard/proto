import pygame
from settings import *

class Clock():

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.time = pygame.time.get_ticks()
        self.state = 'DAY'
    
    def update(self):
        self.time = pygame.time.get_ticks() % 24000
        if self.state == 'DAY' and self.time >= 10000:
            self.state = 'NIGHT_FALL'
        elif self.state == 'NIGHT_FALL' and self.time >= 12000 :
            self.state = 'NIGHT'
        elif self.state == 'NIGHT' and self.time >= 22000 :
            self.state = 'SUN_RISE' 
        elif self.state == 'SUN_RISE' and self.time <= 11000:
            self.state = 'DAY'
        # TODO log en cas de mauvais resultat

    def draw(self):
        self.update()
        filtre = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA, 32)
        filtre = filtre.convert_alpha()
        if self.state == 'NIGHT_FALL':
            color = self.night_fall()
            filtre.fill(color)
            self.display_surface.blit(filtre, (0,0))
            return
        if self.state == 'NIGHT':
            filtre.fill((0,0,10,230))
            self.display_surface.blit(filtre, (0,0))
            return
        if self.state == 'SUN_RISE':
            color = self.sun_rise()
            filtre.fill(color)
            self.display_surface.blit(filtre, (0,0))
            return

    def night_fall(self):
        moment = 12000-self.time
        color = [0,0,10,0]
        color[3] = 230 - moment*230/2000
        return color
    
    def sun_rise(self):
        moment = 24000-self.time
        color = [0,0,10,0]
        color[3] = moment*230/2000
        return color
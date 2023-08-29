from enum import Enum

import pygame

from settings import *
from debug import debug

class DayState(Enum):
    DAY = 'DAY'
    NIGHT_FALL = 'NIGHT_FALL'
    NIGHT = 'NIGHT'
    DAY_RISE = "DAY_RISE"

time_limite_dict = {
    DayState.DAY : 10000,
    DayState.NIGHT_FALL : 2000,
    DayState.NIGHT : 10000,
    DayState.DAY_RISE : 2000
}

class DayCycle():

    def __init__(self,light_group, state = DayState.DAY):
        self.display_surface = pygame.display.get_surface()
        self.time = pygame.time.get_ticks()
        self.state = state
        self.time_limite_dict = time_limite_dict
        self.time_limite = self.time_limite_dict[self.state]
        self.offset = self.time

        self.light_group = light_group
    
    def update_state(self):
        ticks = pygame.time.get_ticks()
        debug(self.time,100)
        if self.time >= self.time_limite :
            match self.state :
                case DayState.DAY:
                    self.state = DayState.NIGHT_FALL
                case DayState.NIGHT_FALL:
                    self.state = DayState.NIGHT
                case DayState.NIGHT:
                    self.state = DayState.DAY_RISE
                case DayState.DAY_RISE:
                    self.state = DayState.DAY
            self.offset = ticks
            self.time_limite = self.time_limite_dict[self.state]
        self.time = pygame.time.get_ticks() - self.offset

    def change_state(self, state):
        self.state = state
        self.offset = self.time
        self.time_limite = self.time_limite_dict[self.state]

    def draw(self):
        match self.state:
            case DayState.NIGHT_FALL:
                color = self.night_fall()
                filtre = self.draw_filter(color)
                self.display_surface.blit(filtre, (0,0))
            case DayState.NIGHT:
                color = (0,0,10,230)
                filtre = self.draw_filter(color)
                self.display_surface.blit(filtre, (0,0))
            case DayState.DAY_RISE:
                color = self.sun_rise()
                filtre = self.draw_filter(color)
                self.display_surface.blit(filtre, (0,0))

    def night_fall(self):
        color = [0,0,10,0]
        color[3] = self.time*230/self.time_limite_dict[DayState.NIGHT_FALL]
        return color
    
    def sun_rise(self):
        color = [0,0,10,0]
        color[3] = 230 - self.time*230/self.time_limite_dict[DayState.DAY_RISE]
        return color
    
    def draw_filter(self, color):
        filtre = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA, 32)
        filtre = filtre.convert_alpha()
        filtre.fill(color)
        self.light_group.add_light(filtre)
        return filtre
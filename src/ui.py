import pygame
from settings import *

class UI:
    def __init__(self):
        
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        #convert weapon dictionnary
        self.weapon_graphics = []
        for weapon in weapons_data.values():
            path = weapon['graphic']
            self.weapon_graphics.append(pygame.transform.scale(pygame.image.load(path), (16 *4 , 16 * 4)).convert_alpha())

    def show_bar(self, current_amount, max_amount, bar_width, position, color):
        #draw background bar
        x, y = position[0] + 6, position[1] - BAR_HEIGHT/2
        bg_bar_rect = pygame.Rect(x, y, bar_width, BAR_HEIGHT)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_bar_rect)

        #draw bar
        ratio = current_amount / max_amount
        current_width = bg_bar_rect.width * ratio
        current_rect = bg_bar_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_bar_rect, 3)

    def show_health(self, current_amount, max_amount):
        heart_surf= pygame.transform.scale(pygame.image.load(HEART_ICON), (16 * 2, 16 *2)).convert_alpha()
        heart_rect = heart_surf.get_rect(topleft = (10, 10))

        position = heart_rect.midright

        self.display_surface.blit(heart_surf, heart_rect)
        self.show_bar(current_amount, max_amount,  HEALTH_BAR_WIDTH, position, HEALTH_COLOR)

    def show_gold(self, gold_amount):
        x, y = self.display_surface.get_size()[0] - 20,  self.display_surface.get_size()[1] - 20
        coin_surf = pygame.transform.scale(pygame.image.load(COIN_ICON), (16 * 2, 16 *2)).convert_alpha()
        coin_rect = coin_surf.get_rect(bottomright= (x,y))

        position = coin_rect.midleft
        offset_with_icon = 6
        x, y = position[0] - offset_with_icon, position[1]

        text_surf = self.font.render(str(int(gold_amount)), False, UI_TEXT_COLOR)
        text_rect = text_surf.get_rect(midright = (x, y))

        width_rect = text_rect.width + offset_with_icon + coin_rect.width - 4
        height_rect = coin_rect.height
        x_rect, y_rect = text_rect.midleft
        y_rect = y_rect  - height_rect/2
        
        bg_rect =  pygame.Rect(x_rect, y_rect, width_rect, height_rect)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect.inflate(20, 10))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect.inflate(20, 10), 3)

        self.display_surface.blit(coin_surf, coin_rect)
        self.display_surface.blit(text_surf, text_rect)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if has_switched :
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(10, self.display_surface.get_size()[1] - 10 - ITEM_BOX_SIZE, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def display(self, player):
        self.show_health(player.health, player.stats['health'])
        self.show_gold(player.gold)
        self.weapon_overlay(player.weapon_index,  not player.can_switch_weapon)
        
        

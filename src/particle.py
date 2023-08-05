import pygame
from os import walk
from settings import *


class AnimationPlayer:
    def __init__(self):
        self.frames = {
            #attacks
            'claw' : self.import_graphics('assets\particles\claw'),
            'slash' : self.import_graphics('assets\particles\slash'),
            'sparkle' : self.import_graphics('assets\particles\sparkle'),
            'leaf_attack' : self.import_graphics('assets\particles\leaf_attack'),
            'thunder' : self.import_graphics('assets/particles/thunder'),
            
            # monster deaths
            'smoke' : self.import_graphics('assets/particles/smoke'),
            
            # leafs
            'leaf' : (
                    self.import_graphics('assets/particles/leaf1'),
                    self.import_graphics('assets/particles/leaf2'),
                    self.import_graphics('assets/particles/leaf3'),
                    self.import_graphics('assets/particles/leaf4'),
                    self.import_graphics('assets/particles/leaf5'),
                    self.import_graphics('assets/particles/leaf6'),
                    self.reflect_images(self.import_graphics('assets/particles/leaf1')),
                    self.reflect_images(self.import_graphics('assets/particles/leaf2')),
                    self.reflect_images(self.import_graphics('assets/particles/leaf3')),
                    self.reflect_images(self.import_graphics('assets/particles/leaf4')),
                    self.reflect_images(self.import_graphics('assets/particles/leaf5')),
                    self.reflect_images(self.import_graphics('assets/particles/leaf6')))}

    def reflect_images(self, frames):
        new_frames = []
        for frame in frames:
            fliiped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(fliiped_frame)
            
        return new_frames
    
    def import_graphics(self, path):
        surface_list = []
        
        for _,__,img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)

        return surface_list

    def create_particle(self, position, particle_type,  groups):
        animation_frames = self.frames[particle_type]
        Particle(position, animation_frames, groups)
        
    
    
    
    
    
class Particle(pygame.sprite.Sprite):
    def __init__(self, position, animation_frames, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = position)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            
    def update(self):
        self.animate()
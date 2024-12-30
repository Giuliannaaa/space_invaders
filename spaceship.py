import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        original_image = pygame.image.load("Graphics/spaceship.png")
        self.image = pygame.transform.scale(original_image, (40, 41))
        
        self.rect = self.image.get_rect(midbottom = (self.screen_width//2, self.screen_height - 70))
        self.speed = 6
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        
    def get_user_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE]:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            
    def update(self):
        self.get_user_input()
        self.constraint_movement()
        self.lasers_group.update()
        self.recharge_laser()
        
    def constraint_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset
            
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True
    
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height - 70))
        self.lasers_group.empty()
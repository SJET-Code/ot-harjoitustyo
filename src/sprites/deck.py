import pygame
from image_loader import load_sprite

class Deck_Sprite(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0):
        super().__init__()
        self.image=load_sprite('Deck')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
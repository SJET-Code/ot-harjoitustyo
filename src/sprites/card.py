import pygame
from image_loader import load_sprite

class Card(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, card=""):
        super().__init__()
        self.image=load_sprite(card)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
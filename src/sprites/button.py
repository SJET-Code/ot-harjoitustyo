import pygame
from image_loader import load_sprite


class Button(pygame.sprite.Sprite):
    def __init__(self, x_position=0, y_position=0, button=""):
        super().__init__()
        self.image = load_sprite(button+'_button')
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def width(self):
        return self.image.get_width()

    def height(self):
        return self.image.get_height()
